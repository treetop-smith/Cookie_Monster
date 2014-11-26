# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 14:06:13 2014
spatula development notes

This file includes several scripts for scraping information from an AllRecipes.com
url. The most powerful of which is the .wrap() module which takes all of the 
information that can be scraped by this program and puts it into a formatted
text file named after the recipe. The information currently provided is as follows:
Recipe Name
Recipe Description
Serving Size
Prep Time
Cooking Time
Ingredients
Directions
Nutritional Information

"""


from BeautifulSoup import BeautifulSoup
import re
import sys

"""
#This is the debugging information so that you can have a url to play with
#if you need to 
url = "http://allrecipes.com/Recipe/Marbled-Pumpkin-Cheesecake/"
#url="http://allrecipes.com/recipe/banana-banana-bread/"
page_html_raw = urlopen(url).read()
soup = BeautifulSoup(page_html_raw)
"""

#This function returns a string of the name of the recipe
def get_Name(soup):
    name_html=soup.find("p", {"class" : "recipeTitle"})
    name=name_html.renderContents()
    return name.replace('<span id="lblTitle">','').replace('</span>','')

#This function gets the description of the recipe 
def get_Description(soup):
    description_html=soup.find(id="metaDescription")
    description=description_html.prettify()
    chopped=description[55:len(description)-5]
    return chopped
#This function returns a list of strings that are the ingredients and their
#quantities
def get_Ing(soup):
    ing_amt=soup.findAll(id="lblIngAmount")  
    ing_name=soup.findAll(id="lblIngName")
    ing_list=[]
    if len(ing_name)==len(ing_amt):      
        for line in ing_amt:
            ing_list.append(line.renderContents())
        i=0
        for line in ing_name:
            ing_list[i]=ing_list[i]+' '+line.renderContents()
            i=i+1
    return ing_list

#This function returns a string that has the prep time for the recipe     
def get_Prep_Time(soup):
    prep_Time_html=soup.find(id="prepMinsSpan")
    holder=prep_Time_html.renderContents()
    holder_2=holder.replace("<em>","").replace("</em>","")
    prep_Time="Prep Time is "+holder_2
    return prep_Time
    
#This function returns a string that has the cook time for the meal    
def get_Cook_Time(soup):
    cook_Time_html=soup.find(id="cookMinsSpan")
    holder=cook_Time_html.renderContents()
    holder_2=holder.replace("<em>","").replace("</em>","")
    cook_Time="Cook Time is "+holder_2
    return cook_Time
   
#This function returns a list of strings that represent each of the discrete
#direction steps in order
def get_Directions(soup):
    directions_html=soup.findAll("span", {"class" : "plaincharacterwrap break"})
    directions_list=[]
    for line in directions_html:
        directions_list.append(line.renderContents())
    sub_directions=[]
    for line in directions_list:
        temp=line.split('.')
        for item in temp:           
            sub_directions.append(item)  
    sub_directions=filter(None,sub_directions)
    i=0
    for item in sub_directions:
        if item[0]==" ":
            sub_directions[i]=item[1:len(item)]
        i=i+1;
    return sub_directions
#This function returns a list of strings that that have the number of calories,
#total cholesterol, amount of fiber, amount of sodium, total carbohydrates,
#the fat and protein
def get_Nutrition(soup):
    categories=soup.findAll("li", {"class" : "categories"})
    units=soup.findAll("li", {"class" : "units"})
    nutrient_List=[]
    if len(categories)==len(units):
        for line in units:
            nutrient_List.append(line.renderContents().replace('<span id="lblNutrientValue">','').replace('</span>',''))
        i=0
        for line in categories:
            nutrient_List[i]=nutrient_List[i]+' '+line.renderContents()
            i=i+1
    return nutrient_List

#This Function returns a string stating the number of servings
def get_Servings(soup):
    servings_html=soup.find("span", {"itemprop" : "servingSize"})
    servings="The serving size is "+servings_html.renderContents()
    return servings

#This wraps the recipe information into a text file that is named after the 
#recipe name (once that name has been normalized to ensure it is a valid file
#name)
def wrap(soup):
    recipe_name=get_Name(soup)
    description=get_Description(soup)
    ingredients=get_Ing(soup)
    prep_time=get_Prep_Time(soup)
    cook_time=get_Cook_Time(soup)
    directions=get_Directions(soup)
    nutrition=get_Nutrition(soup)
    servings=get_Servings(soup)
    #turn the recipe name into a format suitable for a file name
    file_name=(recipe_name.replace(' ','').replace('/','').replace('?','')
    .replace('?','').replace('%','').replace('*','').replace(':','')
    .replace('"','').replace('<','').replace('>','').replace('.',''))
    file_name=file_name+".txt"
    fo=open(file_name,'w')
    fo.write(recipe_name)
    fo.write("\n")
    fo.write(description)
    fo.write("\n")
    fo.write(servings)
    fo.write("\n")
    fo.write(prep_time)
    fo.write("\n")
    fo.write(cook_time)
    fo.write("\nIngredients")
    for item in ingredients:
        fo.write("\n")
        fo.write(item)
    fo.write("\nDirections")
    i=1
    for item in directions:
        fo.write("\n"+str(i)+") ")
        fo.write(item)
        i=i+1
    fo.write("\nNutritional Information per Serving")
    for item in nutrition:
        fo.write("\n")
        fo.write(item)
    fo.close()
 
#More testing   
