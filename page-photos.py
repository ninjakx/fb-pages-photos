import json
import os
from urllib import urlopen
import facebook
from xvfbwrapper import Xvfb
from selenium import webdriver
from PIL import Image
import cStringIO

ID = '' #Put id of the page

TOKEN = '' #Put ur access token

def create_dir(fname): 
    global filename 
    filename=fname
    if not os.path.isdir(filename):
        os.mkdir(filename)
    os.chdir(filename)

def save_and_download(object_id):
    global count
 
    display = Xvfb()#Hide the browser
    display.start()
    url='https://graph.facebook.com/'+object_id+'/picture'

    chromedriver_loc = '/path/to/chromedriver'  # enter path of chromedriver

    driver = webdriver.Chrome(executable_path=chromedriver_loc)
    
    driver.get(url)
    cur_url=driver.current_url
    if cur_url!=url:  #If object_id is directing to image page
        count+=1
        imgdata = urlopen(cur_url).read()               #save the image
        img = Image.open(cStringIO.StringIO(imgdata))
        img.save(retval+'/'+str(count)+".png")
 
    driver.quit()
    display.stop()

def fetch(limit, depth, id=ID, token=TOKEN):

    """Fetch the data using Facebook's Graph API"""
    
    graph = facebook.GraphAPI(token)
   
    url = '%s/photos/uploaded' % id
   
    args = {'limit': limit}
    res = graph.request('%s/photos/uploaded' % id, args)
    #print(res)
    process(res['data'],depth)
 
def process(dat,depth):
    
    img = []
    obj=len(dat)
    
    '''take <depth> objects at a time'''
 
    generator = (i for i in xrange(obj)) #Generate no. from 1 to limit
    for k in range(obj//depth + 1):
        
        loop=(list(next(generator) for _ in range(depth)))
        for d in loop:
            if 'name' in dat[d]:   #If image has caption or decription save it in the folder
   
                save_and_download(dat[d]['id'])
 
if __name__ == '__main__':
   
    fname=str(raw_input("Enter filename : "))
    create_dir(fname) #create directory
    global retval
    #gives the  current location of the folder
    retval = os.getcwd() 
    count=0
    
    fetch(1067,32)    #fetch(limit,depth)
    print("done")
    #limit:no of photos you want to download
    #depth:take <number> of photos at a time then move to next slot


