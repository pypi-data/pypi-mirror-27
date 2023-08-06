# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:18:51 2017

@author: SKT
"""

import requests
import base64
import matplotlib.pyplot as plt
import cv2
import numpy as np
import json

#supporting functions
def hex_to_rgb(hexCode):
    hexCode = hexCode.lstrip('#')
    return list(int(hexCode[i:i+2], 16) for i in (0, 2 ,4))

#main functions
def dominantColors(imagePath, clusters = 5):
    URL = 'http://skt7.pythonanywhere.com/api'
    
    #send base64 data
    img = base64.b64encode(open(imagePath, 'rb').read())
    
    response = requests.post(URL, data={ 'img' : img, 'clusters' : clusters})
    
    return response.text

def plotColors(data):
    
    data = json.loads(data)
    
    colors = []
    hist = []
    
    for i in data:
        colors.append(hex_to_rgb(i))
        hist.append(data[i])
    
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0
   
    for i in range(len(colors)):
		# plot the relative percentage of each cluster
        endX = startX + (hist[i] * 300)
        red = int(colors[i][0])
        green = int(colors[i][1])
        blue = int(colors[i][2])
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), (red,green,blue), -1)
        startX = endX	
    
	# return the bar chart
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()
