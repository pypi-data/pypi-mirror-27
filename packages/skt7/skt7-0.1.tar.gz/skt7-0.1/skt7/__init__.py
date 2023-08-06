# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:18:51 2017

@author: SKT
"""

import requests
import base64

def dominantColors(imagePath):
    URL = 'http://skt7.pythonanywhere.com/api'
    
    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    
    #send base64 data
    img = base64.b64encode(open(imagePath, 'rb').read())
    response = requests.post(URL, data=img, headers=headers)
    
    return response.text

