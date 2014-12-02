# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 08:17:43 2014
Fruitfly development notes
This module goes to the Allrecipes.com list of recipes, starting from the
top rated recipe, and proceeds to pull out each of the links, including the 
link to the next page. It then scrapes each of those links using spatula, 
which is the scraper that produces the txt file from the recipe, and saves it
@author: smithm
"""
from BeautifulSoup import BeautifulSoup
import re
import sys
from urllib import urlopen
import spatula

def pageLinks(soup):    
    html_list=soup.findAll("h3", {"class" : "resultTitle"})
    recipe_urls=[]
    for item in html_list:
        recipe_urls.append(item.renderContents())
        print(recipe_urls)
    for i in range(0,len(recipe_urls)):
        hacked=recipe_urls[i].split('"')
        recipe_urls[i]=hacked[3]
    print(recipe_urls)
    return recipe_urls      
    
pageNum=1
nextPage=True
while nextPage==True:
    currentPage="http://allrecipes.com/recipes/main.aspx?vm=l&evt19=1&p34=HR_ListView&Page="+str(pageNum)+"#recipes"
    page_html = urlopen(currentPage).read()
    url_soup = BeautifulSoup(page_html)
    
    url_list=pageLinks(url_soup)
    for recipe_url in url_list:           
        recipe_html=urlopen(recipe_url).read()
        recipe_soup =BeautifulSoup(recipe_html)
        spatula.wrap(recipe_soup)
    is_next=url_soup.find("link", {"rel" : "next"})
    nextPage=False
    """
    try: 
        len(is_next)
        nextPage=True
        pageNum=pageNum+1
    except TypeError:
        nextPage=False
    """


    
