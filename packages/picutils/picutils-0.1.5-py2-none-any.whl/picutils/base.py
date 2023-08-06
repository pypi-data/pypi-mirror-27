# -*- coding:utf-8 -*-

from __future__ import print_function
import os
import sys
import webbrowser
from PIL import Image
from time import time
from natsort import natsorted
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
import shutil


try:
   input = raw_input
except NameError:
   pass


Format = ['bmp', 'gif', 'jpg', 'png', 'jpeg']
basewidth = 200



# single file convert format to jpg
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

# single file shrink image size                
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

# multi-processing shrink size to folder of pics       
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

# multi-processing convert to jpg to folder of pics 
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
    

# starter of processing pics
def process_pics():
   
    """pass paras: pic folder PATH, if convert to jpg(y/n), if shrink size(y/n)"""
    
    print('Batch processing images in a folder')
    if len(sys.argv)==4:
        
        path, flag1, flag2 = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        path = str(input("PATH of folder contains pics: "))

        flag1 = str(input("convert pics formats to jpg? (y/n): "))
        flag2 = str(input("shrink pics size? (y/n): "))


        
    if not path.strip():
        return 
          
    d = os.listdir(path)
    e = [i for i in d if i.find('.')>0]
                    
    if flag1=='y':
        convert2jpg(e)
    if flag2=='y':
        multi_shrink(e)    
                    

# delete a folder (for running fast in windows)
def del_entire_folder():            
    path = str(input(('folder path to delete(fast in windows): ')))
    if not path.strip():
        return
    shutil.rmtree(path)
        

                    
                    
# create html viewer for a folder of images        
def html_viewer():
    """pass folder PATH, create a html viewer for a folder of images"""
    
    #print('Batch indexing images to html')
    if len(sys.argv)==2:
        
        path = sys.argv[1]
    else:
        path = str(input("PATH of folder contains pics: "))
        
    if not path.strip():
        return

    cwd = os.path.abspath(path)[:-len(path)]
    # print(repr(cwd))
    

    filename=cwd+path
    # print(repr(filename))
    

    names = os.listdir(filename)
    

    having=[]
    for i in names:
        if i.split('.')[-1].lower() in Format:

            having.append(filename+'/'+i)


    having=natsorted(having)
    having=str(having)





    web="""

    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>image viewer</title>
    </head>
    <body onload = "pNext()">

    <script language="javascript" type="text/javascript">


        having=%s;"""%having+"""

        var starting=having.length*10000-1;



        function sSetHtml(x){

            x=x%having.length;
            display=x+1;

            document.getElementById("num").innerHTML=("<h2><font color=crimson>"+display+" </font>/<font color=grey>"+having.length+"</font></h2>");

            document.getElementById("pDisk").innerHTML=
                "<div style=position: relative;><img id='what' src='" + having[x] + "' style='position: absolute;margin: auto;top: 0;bottom: 0;left: 0;right: 0;max-width: 100%;max-height: 100%;'/></div>";
        }

        function pBack(){

        starting--;
        sSetHtml(starting);
        
        }

        function pNext(){

        starting++;
        sSetHtml(starting);

        }




    </script>

    <div style="margin:auto; border: 1px solid purple;width:98%; height:98%; position:absolute">


        <a title='previous' href="javascript:pBack();" style="background:url('') no-repeat;
        opacity:0.001;
        width:42%; height:94%; z-index:9999; position:absolute; cursor:url('data:image/jpg;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADmElEQVRYhbXXW4hVVRgH8N8cBjERkZAwkbaItyQiepIKYidK9GbWm0RFljsR6W5UTwZF5kN02Zk9iEEQguWbKLVepHwQCQnBy4NbZQKRiGGYZJChh7U2Z890zpytjR9s1l7X//9bl+8ypKXkRTUXTyDHQ1iBBZjAGK7iNH7GL6HMbrRZd6gF8BK8gedxd0u+f+Eg9oQyG7ktAnlRDeNtvId5ja6LOIFzCaiDhbgf67CqMXYcH+HjUGY3WxNIWh/CI42FvsX+UGZ/zKRRXlRr8QpeahA/ic29duM/BPKiWiGe432p6TB2hjK7OhNwHyU+wzOp6TI2hDI735dAXlSL8RuW4SZ2hDL7+laAexDZhs8xnEg82lRmqDFwGAGPJfBnQ5n99H/AG2s/jR8SiZN4PJTZBPEC1fJmAidqPivgEMrsMHak6jrsqvuGEsPFuID5OBzKbPNMC+ZFRdSmlslQZpODiORFdUi8EzewMpTZ1XoH3krg49jZAvxL/JO+K3hgEHiSnaLRmpswDeVFNQd/ikbmi1BmO/rNboC/mpquY30oszMtCciLai9ex9+4tyOa19rC7buT4NMwFmJjB+tTw/l+RmYWwSU7cDZVN3RExwK/3mnwhpxI5cPDuhbvQgtwmIMjqa+NFKHMjk5rO5fKZcPiWRAvxSBwogte0BbdVEdWy/W6r2mIer3jTo+2WZUORtP/omZHKDPYjum+YCLNafv1csP1qxsfFiOZFVg5fVQos8m8qLan6rZUXkMeyuxiGw37yOpUXu7g91RZ12tkMrHNnViKkNz27UodZ5zqiB4QVuVFteZOk8iLarmu6Q4dHNN9AVv7TZxFElvFuzeGY50UvR5InS8nzziIxFfi5VqM40mrgZIX1SLdu3QwlNlY/cz2iJ5wPvbOtEiDxF3pW4lLbQiktReK7ngPUyOi97E7VV8IZXag5aKtJC+qLfguVT8MZfYBUw3NJziV/vflRfXULIJvxP5UPa2raJdAitE2YUS09z/mRfXiLIBvwRExCBnBpjoepHdYvgbHxVsO3+O1UGbXbhH4HvGcn0tNI2JYfrY5rl9islRMTGrjNIpvxMTkfK85jbnLxcRkm67TOiUmJpenjx+Umu3Cu6Z6tLNi7HBOtB+T4s1eLVq4tbpHewOfYndz21sRaBBZgnfE5LStGx7TTU4vzTRwIIEGkXl4UgzhHhQDmZrQqJj1nBHTuqOhzMbbrPsvL9JL7lKnILsAAAAASUVORK5CYII='),pointer; left:0px; top:30px;background-color:powderblue;"></a>


        <a title="next" href="javascript:pNext();"  style="background:url('') no-repeat;
        opacity:0.001;
        width:55%; height:95%; z-index:9999; position:absolute; cursor:url('data:image/jpg;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADgUlEQVRYhbXXQWgdVRQG4C+PEIMEqSVIiaHMSKulSBddSO1GMVZciIg14EpcJCVBapDqoBQEF0UZjCIasbWLLJW24MKdbV0oVbqQ4qLaKs6gQbuQkkXQUIK4uPf5Ji/PvHltcmB4c++7c/7/3HvOPef0qSllmg/gERzAXtyDIdzAEhbwHb7A+aTIbtTR21cDeARH8Dy21uR7HfOYTYrs95siEC1+GUdxe+Wvq7iAHyIQDGMn9mNXZe1fOIY8KbKV2gTKNB/FKeyrKDqJ40mRXV7PojLNd2EaExXi3+Jgp91YQ6BM83txDqNx6jRmum1lBz0jeB9Px6lfcSApsqv/SyBa/k0EX8ELSZGd6AW4A5GpSKQ/kniwakxfZeEAvsIDEXw8KbLPbgW8ovspfIoBwX8eavpEo7Lu1QhOsHxDwCHqOhyH+wXnRtyBuPVXBKc5nRTZeDelZZo3rDZgJSmybt+cwjPCvbEzKbJrTQWvRPAlzHS3CezGb/g7PnOR1HoyI0TUkHC36CvTfBB/YAveSYrsSE0CyjTfI0TMcJz6SDi+f9b55j28iD9xdwOPRnA4XhcckiL7HmNRGUzpvhNNjGE83BDudvixPUY3g0S8yH6Ow7GGkFjg617Bb5aEEIqwtx/b4+BK+6oyzR/Hxz1wGay8T0UdnXyiiZX0Cx5JK7G0KxztMF9XmiSm20K0ibWlW9hshHSKiCZuo1+Iy6065/oVLPYANmj1MXwohGX7uibWYj9+Ebb5vvZVSZF9jjvrIMcs+iVGuoATagcoG0IZRSv39yw9ghPyAVxqCDUc3F+m+Y7NBi/TfDeaOOcaOKt1ztObCR5lMv5ex/lGrF7n4+ShMs231QTfIezeXYKzftANPFZJE3E4nxTZcjMc3sWycCfM1iEgOG+K2+JzuFs6jjhDQtadZXVF9AZej8PJpMhO1iRSS8o0n9C6VV9LiuwtVhcUx3Axvs+Vaf7EBoI/ibk4vIC3m//9RyD6wkGhwxnAmcj6VsEnhBJ/QChKx6s9Qp2y/BO8lBTZtR6Btwln/mycWsDYumV55eNRnNEqUpdwQmhM1q0ZYmMyiUNaie6i0JgstK/v1podRWb1/X5ZOMeftO6PZmu2z9rW7E2hNevYrNZpTrcLRetzuKPb+iiLWs3pGqt7IlAhMojHhMpnD5IKoUXBwS4J/nM2KbLlOnr/BfusOqMTocbTAAAAAElFTkSuQmCC'),pointer; right:0px; top:30px;background-color:purple;"></a>
        <p id="num" style="position:absolute top:0px;"></p>
        <a id="pDisk"></a>
        <a href="http://uconn.science" target="_blank" style="color:orange; position: absolute; bottom:0px">&copy</a>

    </div>


    </body>
    </html>
    """

    dest=filename+'_viewer.html'

    with open(dest,'w+') as fh:
        fh.write(web)


    #print(os.path.basename(filename))
    print('done! Saved as: '+dest)
    if input('do you want to open the viewer just created? (y/n) :')=='y':
        try:
            webbrowser.open('file://'+os.path.realpath(dest))
            print("Thank you!")
        except:
            print("Thank you!")
    else:
        print("Thank you!")
        
# move files from a folder (1 leyer)        
def move_out():

    if len(sys.argv)==2:

        path = sys.argv[1]
    else:
        path = str(input("PATH of folder contains pics: "))
        
    if not path.strip():
        return

    save=path



    dest = save+'_out'
    try:
        os.mkdir('./'+ dest)
    except:
        print(dest+' exists')

    flag = input('NOT rename files with subfolder prefix? y:Not rename, n:rename :')
    flag = False if flag=='y' else True

    if input('Move or Copy? y:Copy, n:Move :')=='y':
        func2exec=shutil.copy
    else:
        func2exec=shutil.move


    content = os.listdir('./'+save)

    for i in content:
        if os.path.isdir('./'+save+'/'+i):
            for j in os.listdir('./'+save+'/'+i):
                try:
                    func2exec('./'+save+'/'+i+'/'+j, './'+dest+'/'+(i+'_')*flag+j)
                except Exception as e:
                    print (e)
                    # print('X', end='')
        else:
            try:
                func2exec('./'+save+'/'+i, './'+dest)
            except Exception as e:
                print (e)
                # print('X', end='')
                
                
                
                
                
# thumbnail single file                
def thumb(one):
    
    if True:

        try:
            img = Image.open(cwd+path7+'/'+one)

            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            



            

            name = os.path.basename(one)
            

            dest = cwd+path7+'/thumbnail/' + name.split('.')[:-1][0] + '_re.jpg'


            img.save(dest)
            print ('%',end='')
        except Exception as e:
            print (e,end='')
            






# create html index for a folder of images
def html_index():
    """parameters: path, background color"""
    global path7, cwd

    
    
    color=None
    if len(sys.argv)==2:
        
        path7 = sys.argv[1]

    elif len(sys.argv)==3:
        path7, color = sys.argv[1], sys.argv[2]
    else:
        path7 = str(input("path7 of folder contains pics: "))
        
    if not path7.strip():
        return

    cwd = os.path.abspath(path7)[:-len(path7)]
    # cwd = cwd.replace('\\\\','/')
    # print(repr(cwd))


    contents=os.listdir(cwd+path7)


    if not os.path.exists(cwd+path7 + '/thumbnail'):


        os.makedirs(cwd+path7 + '/thumbnail')

    else:

        print('thumbnail folder exists')


    contents = [k for k in contents if k.split('.')[-1].lower() in Format]

    start = time()


    pool = ThreadPool(cpu_count())

    results = pool.map(thumb, contents)

    pool.close()
    pool.join()

    end = time()

    elapse = end - start


    print ('\n' + str(len(contents) - 1) + ' pics total: %.3fs' % float(elapse))
    print ('per pic: %.3fs' % (elapse / float(len(contents))))




# make index html
    try:
        contents=natsorted(contents)
    except:
        print('not sorted')


    fh = open(cwd+path7 + '_index.html', 'w+') 

    color='white' if not color else color
    web = '<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"/>\
<title>your photos</title></head>\
<font color="purple"><div class="text" style="text-align:center;">\
    <h2> image index for {} </h2></div></font><body bgcolor="{}">'.format(path7,color)

    for pic in contents:
        # print(repr(cwd))

        web += '<a href="' + cwd + path7 + '/' + pic + '">' + \
                '<img src="' + cwd + path7 + '/thumbnail/' + ''.join(pic.split('.')[:-1])+'_re.jpg" title="view'+pic+'" width=200 />&nbsp;</a>'


    web += '<a href="http://uconn.science" target="_blank" style="color:orange;">&copy</a></body></html>'

    fh.write(web)
    fh.close()

    print('done! Saved as: '+path7 + '_index.html')
    if input('do you want to open the html index just created? (y/n) :')=='y':
        try:
            webbrowser.open('file://'+os.path.realpath(path7 + '_index.html'))
            print("Thank you!")
        except:
            print("Thank you!")
    else:
        print("Thank you!")