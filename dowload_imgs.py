# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 10:51:52 2019

@author: quang
"""

import re
import requests

# it is crucial to use this specific user_agent, since this webpage uses cloudflare to avoid ddos attack
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'



s = requests.Session()

page_idx = 0
img_idx = 1
numb_idx = 1

while True:
    site = "http://platesmania.com/us/gallery.php?&region=7505&start={}".format (page_idx)
    print ("Connecting to {}".format (site))
    try:
        response = s.get(site, headers={'user-agent': user_agent})
        cookies = dict (response.cookies)
        
        print ("\n\n---------\nAnalyzing the webpage...")
        
        print ("\n-> Download plate images")
        img_tags = re.findall ('img .*?src="(.*?)"', response.text)
        for url in img_tags:
            if url.find ("/m/") != -1:
                print (url)
                f = open ("D:/LPR_Dataset/Download_img/imgs/{}.jpg".format (img_idx), "wb")
                img = s.get(url, headers={'user-agent': user_agent})
                f.write (img.content)
                f.close()
                img_idx += 1
                
        print ("\n\n-> Extract the plate number")
        numb_tags = re.findall ('img .*?alt="(.*?)"', response.text)
        for number in numb_tags:
            print ("***** Extracted number: {}".format (number))
            #if number == "":
            #    f = open ("D:/LPR_Dataset/Download_img/annotations/{}_check.txt".format (numb_idx), "w")
            if (len (number) < 10) and (number != ""):
                f = open ("D:/LPR_Dataset/Download_img/annotations/{}.txt".format (numb_idx), "w")    
                numb_idx += 1
            else:
                continue
                
            f.write (number)
            f.close()
                
    except requests.exceptions.ConnectionError:
        print ("Connection refused")
        
    except requests.exceptions.InvalidURL:
        break
    
        
    
    page_idx += 1
    
    if page_idx == 101:
        break
