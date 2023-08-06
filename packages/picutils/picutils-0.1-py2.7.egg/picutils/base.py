# -*- coding:utf-8 -*-

from __future__ import print_function
import os
import sys
from PIL import Image
from time import time
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool



try:
   input = raw_input
except NameError:
   pass



Format = ['bmp', 'gif', 'jpg', 'png', 'jpeg']

def convert(file):

    file=path+'/'+file
    extension = os.path.splitext(file)[1]

    if extension=='.JPG':
        try:
            os.rename(file, file[:-3]+'jpg')
        except:
            print ('X', end='')
            
    extension = extension.lower()[1:]    
    if extension in Format:
        if extension !='jpg':
            try:
                img=Image.open(file)
                img =  img.convert('RGB')
                print ('!', end='')

                if extension=='jpeg':
                    img.save(file[:-4]+'jpg')
                    os.remove(file)
                else:
                    img.save(file[:-3]+'jpg')
                    os.remove(file)     

            except:
                print ('X', end='')

def shrink(file):

    file=path+'/'+file


    try:
        img=Image.open(file)            
        size=os.path.getsize(file)/1000
    except Exception as e:
        print ('?', end='')

        
    try:
        
        if size>2500:
            rate=25            
        elif size>2000:
            rate=30
        elif size>1500:
            rate=40
        elif size>1000:
            rate=50
        elif size>500:
            rate=60
        elif size>400:
            rate=65
        elif size>300:
            rate=75
        elif size>200:
            rate=80
        elif size>100:
            rate=85
##        elif size>60:
##            rate=90                 
        else:
            rate=100

        
        img.thumbnail((img.size[0]*rate/100, img.size[1]*rate/100))
        img.save(file[:-3]+'jpg')
  
        print ('%', end='')


    except Exception as e:
        print ('X', end='')

def multi_shrink(lis):
    print ('processing pics......')
    
    start=time()
    
    pool = ThreadPool(cpu_count())

    results = pool.map(shrink, lis)

    pool.close()
    pool.join()

    end = time()


    elapse = end - start 
    print ('used {:.2f}s for {} images, {:.2f}s/pic'.format(elapse, len(lis), elapse/len(lis)))
                
def convert2jpg(lis):      
    print ('processing pics......')
    
    start=time()
    
    pool = ThreadPool(cpu_count())

    results = pool.map(convert, lis)

    pool.close()
    pool.join()

    end = time()


    elapse = end - start 
    print ('used {:.2f}s for {} images, {:.2f}s/pic'.format(elapse, len(lis), elapse/len(lis)))   
    
    
def processPics():
   
    """pass paras: pic folder PATH, if convert to jpg(y/n), if shrink size(y/n)"""
    global path
    print('Batch processing images in a folder')
    if len(sys.argv)==4:
        
        path, flag1, flag2 = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        path = str(input("PATH of folder contains pics "))
        flag1 = str(input("convert pics formats to jpg? (y/n)"))
        flag2 = str(input("shrink pics size? (y/n)"))
    
    d = os.listdir(path)
    e = [i for i in d if i.find('.')>0]
                    
    if flag1=='y':
        convert2jpg(e)
    if flag2=='y':
        multi_shrink(e)    
                    
                    
                    
                    
        
