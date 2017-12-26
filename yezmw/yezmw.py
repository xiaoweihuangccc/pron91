#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pron91pkg import httputil
from bs4 import BeautifulSoup
from pron91pkg import disk
import requests
import shutil
import os
# 1.get title
#2.get html5 m3u8
#3.download ts files from m3u8
#4.merge m3u8 to one file(ts file)

basePath = "Spider/yezmw/"

def handleVideoContent(url):
    disk.mkdir(basePath)
    content = httputil.fetchContent(url)

    # print(content)

    soup = BeautifulSoup(content , "html.parser")
    results = soup.find_all("span",class_="title")

    global result
    global title
    global hlsViedoUrl
    if len(results)>0:
        targetSoup = results[0]
        title = str(targetSoup.text)
    results = soup.find_all("div",class_="dz")
    if len(results) >0:
        targetSoup = results[0]
        childSoup = targetSoup.find("p")
        hlsViedoUrl = str(childSoup.text)


    result = {
        "title":title,
        "hlsViedoUrl":hlsViedoUrl
    }
    return result

# url = "http://yezmw.com/video/show/id/4239"
#
# handleVideoContent(url)

def decodeM3u8File(title,hlsVideoUrl):

    folderPath = basePath + title +"/"
    disk.mkdir(folderPath)
    #create floder
    index = hlsVideoUrl.rfind("/")
    targetPath = folderPath+hlsVideoUrl[index+1:]
    baseURL = hlsVideoUrl[:index+1]

    #remove m3u8 file
    try:
        file = open(targetPath, 'r')
        file.close()
        os.remove(targetPath)
    except FileNotFoundError:
        pass

    #remove convert.m3u8 file
    try:
        file = open(folderPath +"convert.m3u8", 'r')
        file.close()
        os.remove(folderPath +"convert.m3u8")
    except FileNotFoundError:
        pass


    #download m3u8 file
    response = requests.get(hlsVideoUrl, stream=True)
    with open(targetPath, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        del response
    #decode m3u8 file
    hlsFile = open(targetPath,"r+")
    outFile = open(folderPath +"convert.m3u8","w+")
    # print(hlsFile.name)

    line = hlsFile.readline()
    lineCount = 0
    while(line!= ''):
        if "#" in line:
            pass
        else:
            line = baseURL + line
            outFile.write(line)
            lineCount = lineCount + 1
        line = hlsFile.readline()



    print("decodeM3u8File end")
    hlsFile.close()
    outFile.close()
    return lineCount

def startdownloadVideo(name,linecount):
    folderPath = basePath + name +"/"
    downloadPath = folderPath + "parts/"
    disk.mkdir(downloadPath)
    downloadFile = open(folderPath+"convert.m3u8","r+")
    line = downloadFile.readline()


    index = line.rfind(".")
    type = line[index:]
    # xxx.ts
    downloadPath = downloadPath + name + type
    # remove xxx.ts file
    try:
        file = open(downloadPath, 'r')
        file.close()
        os.remove(downloadPath)
    except FileNotFoundError:
        pass


    outFile = open(downloadPath,"wb+")
    recordNum = 0;
    while(line!= ''):
        partUrl = line
        recordNum =  recordNum + 1
        print("正在下载片段 " + str(recordNum) + " "+str(recordNum/linecount*100) + "%")

        response = requests.get(partUrl, stream=True)

        outFile.write(response.raw.read())

        del response

        line = downloadFile.readline()
    downloadFile.close()
    outFile.close()
    pass

# hlsVideoUrl ="http://video1.feimanzb.com:8091/20171215/RKI-413-C/550kb/hls/index.m3u8"
# index = hlsVideoUrl.rfind("/")
# targetPath=hlsVideoUrl[index+1:]
# baseURL = hlsVideoUrl[:index+1]
#
# print(targetPath)
# print(baseURL)
# # response = requests.get(hlsVideoUrl, stream=True)
# # with open(targetPath, 'wb') as out_file:
# #     shutil.copyfileobj(response.raw, out_file)
# #     del response

# hlsFile = open(targetPath,"r+")
# outFile = open("convert.m3u8","w+")
# print(hlsFile.name)
#
# line = hlsFile.readline()
# while(line!= ''):
#     if "#" in line:
#         pass
#     else:
#         line = baseURL + line
#         outFile.write(line)
#     line = hlsFile.readline()
#
#
#
# print("end")
# hlsFile.close()
# outFile.close()

# url = "http://video1.feimanzb.com:8091/20171215/RKI-413-C/550kb/hls/gUYZa0Kw2426000.ts"
# index = url.rfind(".")
# print(url[index:])