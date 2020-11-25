import os
import itertools
from PIL import Image
import numpy as np
from os.path import isfile
import copy

#Function to get the names of every folder in a given path (mp)
def onlyfolders(mp):
    return [f for f in os.listdir(mp) if not isfile(mp+chr(92)+f)]

#make a folder
def mk_folder(folder_name):
    path=os.getcwd()
    if folder_name not in onlyfolders(path):
        os.mkdir(path+chr(92)+folder_name)

#here is a function to convert points into an image
def pt_to_im(pt):
    px=[]
    w=(255,255,255)
    b=(0,0,0)
    for i in [0,1,2,3]:
        px.append([])
        for j in [0,1,2]:
            if [j+1,i+1] in pt:
                px[i].append(b)
            else:
                px[i].append(w)


    # Convert the pixels into an array using numpy
    array = np.array(px, dtype=np.uint8)

    # Use PIL to create an image from the new array of pixels
    newsize = (30,40)
    im = Image.fromarray(array)
    im = im.resize(newsize,resample=Image.BOX)
    return im

#move to a corner to compare without taking position into account
def trans(a):
    minax=4
    minay=4
    for i in a:
        if i[0]<minax: minax=i[0]
        if i[1]<minay: minay=i[1]
    return [(i[0]-minax+1,i[1]-minay+1) for i in a]

#rotate by 90 degrees
def rt90(a):
    m=0
    for i in a:
        if i[0]>m: m=i[0]
    return [(i[1],-i[0]+m+1) for i in a]

#compare points
def compare(a,b):
    #print(a,b)
    return set(a)==set(b)


#compare for each rotation
def comp_all(a,b):
    return (compare(a,b) or compare(rt90(a),b) or compare(rt90(rt90(a)),b) or compare(rt90(rt90(rt90(a))),b))

def get_unique(c):
    u=[c[0]]
    for i in c:
        u_b=True
        for j in u:
            if comp_all(trans(i),trans(j)): 
                u_b=False
        if u_b: u.append(i)
    print(len(c),len(u))
    return u



#here are all possible squares to be filled
a=[
[1,1],
[1,2],
[1,3],
[1,4],
[2,1],
[2,2],
[2,3],
[2,4],
[3,1],
[3,2],
[3,3],
[3,4]]

#List of possible combinations for 4 squares
c4=[i for i in itertools.combinations(a,4)]
#for 5
c5=[i for i in itertools.combinations(a,5)]


c4_u=get_unique(c4)
c5_u=get_unique(c5)

#convert the points into images and save them in a folder called 4 and other called 5
it=0
mk_folder("4")
for pt in c4_u:
    #print(it)
    outfile=str(it)+".png"
    pt_to_im(pt).save("4\\"+outfile, "PNG")
    it+=1
it=0
mk_folder("5")
for pt in c5_u:
    outfile=str(it)+".png"
    pt_to_im(pt).save("5\\"+outfile, "PNG")
    it+=1