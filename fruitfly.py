# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 08:17:43 2014
Fruitfly development notes
This module goes to the Allrecipes.com list of recipes, starting from the
top rated recipe, and proceeds to pull out each of the links, including the 
link to the next page. It then scrapes each of those links using spatula, 
which is the scraper that produces the txt file from the recipe, and saves it
The scraper defaults to filling a folder in C:/Recipes, which will be generated
if it does not exist. The user is prompted before the program runs to ensure 
that this is okay with them. The user is then asked whether they want to 
get recipes from just a range of files, or from all available
@author: smithm
"""
from BeautifulSoup import BeautifulSoup
import re
import sys
from urllib import urlopen
import spatula
import os.path

#Created a function that will get all of the links on a page
def pageLinks(soup):    
    html_list=soup.findAll("h3", {"class" : "resultTitle"})
    recipe_urls=[]
    for item in html_list:
        recipe_urls.append(item.renderContents())
    for i in range(0,len(recipe_urls)):
        hacked=recipe_urls[i].split('"')
        recipe_urls[i]=hacked[3]
    return recipe_urls      
#This is the welcome statement
print("Welcome to fruitfly, a web scraper for retriving recipes from Allrecipes.com")


#This code asks the user what directory they want to save to, and then
#ensures that it is a valid directory. If it doesnt exist it will be created
directory="C:/Recipes/"    
print("This program will place the recipes generated in the following default file path,")
print(directory) 
print("which will be generated if necessary")
okay=False   
while okay==False:
    response=raw_input("Is this filepath "+directory+ " okay?(Y/N) ")
    if response=="Y"or response=="y":
        okay=True
        if not os.path.exists(directory):
            os.makedirs(directory)
    elif response=="N"or response=="n":
        directory=raw_input("Okay, what path would you like?: ")
        if not os.path.exists(directory):
            os.makedirs(directory)
        okay=False
    else:
        okay=False

#Now determine how many pages they want to go through
selection=False
while selection==False:
    print("Now, lets figure out what how many recipes are going to be retrived")
    response=raw_input("Would you like to select a range, or retrive all? (range/all) ")
    if response=="range" or response =="Range":
        okay=False
        while okay==False:    
            pageNum=raw_input("What starting page would you like? ")
            pageMax=raw_input("What ending page would you like? ")
            response=raw_input("So you want to search between "+pageNum+ " and "+pageMax+"? (Y/N) ")
            if response=="Y"or response=="y":
                okay=True
            if response=="N"or response=="n":
                okay=False
                print("Okay")
        selection=True
    elif response=="all" or response=="All":
        pageNum=1
        pageMax=1000000 #arbitrarilly large number 
    else:
        print("Unknown response, please retry")
#Starting with a user selected page number, go through each of the links 
#that were scraped, and send that url to spatula to generate the .txt file. 
#It checks if there is another page, and if there isnt it breaks the loop. 
#Otherwise it continues to the next page to grab more links
print("Initiating retrival")
nextPage=True
recipe_count=0
while nextPage==True and pageNum<=pageMax:
    currentPage="http://allrecipes.com/recipes/main.aspx?vm=l&evt19=1&p34=HR_ListView&Page="+str(pageNum)+"#recipes"
    page_html = urlopen(currentPage).read()
    url_soup = BeautifulSoup(page_html)
    url_list=pageLinks(url_soup)
    for recipe_url in url_list:           
        recipe_html=urlopen(recipe_url).read()
        recipe_soup =BeautifulSoup(recipe_html)
        spatula.wrap(recipe_soup,directory)
        recipe_count=recipe_count+1
    is_next=url_soup.find("link", {"rel" : "next"})
    nextPage=False
    try: 
        len(is_next)
        nextPage=True
        pageNum=pageNum+1
    except TypeError:
        nextPage=False
 
print("Completed! A total of "+str(recipe_count)+" recipes were retrived")

    
