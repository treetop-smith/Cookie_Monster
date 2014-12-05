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
import os.path

"""
#This is the debugging information so that you can have a url to play with
#if you need to 
#url = "http://allrecipes.com/Recipe/Marbled-Pumpkin-Cheesecake/"
#url="http://allrecipes.com/recipe/banana-banana-bread/"
url="http://allrecipes.com/recipe/carrot-cake-iii/detail.aspx?evt19=1"
page_html_raw = urlopen(url).read()
soup = BeautifulSoup(page_html_raw)
"""

#This function returns a string of the name of the recipe
def get_Name(soup):
    try:
        name_html=soup.find("p", {"class" : "recipeTitle"})
        name=name_html.renderContents()
        return name.replace('<span id="lblTitle">','').replace('</span>','')
    except:
        return "No Name Listed"
#This function gets the description of the recipe 
def get_Description(soup):
    try:
        description_html=soup.find(id="metaDescription")
        description=description_html.prettify()
        chopped=description[55:len(description)-5]
        return chopped
    except:
        return "No description listed"
#This function returns a list of strings that are the ingredients and their
#quantities
def get_Ing(soup):
    try:
        ing_pairings=soup.findAll("p", {"class" : "fl-ing"})        
        ing_list=[]   
        for line in ing_pairings:
            ing_list.append(line.renderContents())
        i=0
        while i<len(ing_list):
            paired=True    
            if ing_list[i].find('<span id="lblIngAmount" class="ingredient-amount">')==-1 or ing_list[i].find('<span id="lblIngName" class="ingredient-name">')==-1:
                paired=False
            if  paired==False:
                ing_list.remove(ing_list[i])
            else:
                holder=ing_list[i]
                holder=holder.replace('<span id="lblIngAmount" class="ingredient-amount">','')
                holder=holder.replace('<span id="lblIngName" class="ingredient-name">','').replace('</span>','')
                holder=holder.replace('\n',' ')
                holder=holder[1:len(holder)]
                ing_list[i]=holder
            if paired==True:
                i=i+1
        return ing_list
    except:
        return "No ingredients listed"

#This function returns a string that has the prep time for the recipe     
def get_Prep_Time(soup):
    try:
        prep_Min_html=soup.find(id="prepMinsSpan")
        try: 
            holder=prep_Min_html.renderContents()    
            min_len=holder.replace("<em>","").replace("</em>","")
            minutes=True
        except AttributeError:
            minutes=False    
        prep_Hour_html=soup.find(id="prepHoursSpan")
        try:
            holder=prep_Hour_html.renderContents() 
            hour_len=holder.replace("<em>","").replace("</em>","")
            hours=True
            #bug testing
            print("got to prep hours")
            #bug testing
        except AttributeError:
            hours=False
        if hours==True and minutes==True:
            return "Prep Time is "+hour_len+" and "+min_len
        elif hours==False and minutes==True:
            return "Prep Time is "+min_len
        elif hours==True and minutes==False:
            return "Prep Time is "+hour_len
        else:
            return "No prep time listed" 
    except:
        return "No prep time listed"   
#This function returns a string that has the cook time for the meal    
def get_Cook_Time(soup):
    try:
        cook_Min_html=soup.find(id="cookMinsSpan")
        try: 
            holder=cook_Min_html.renderContents()    
            min_len=holder.replace("<em>","").replace("</em>","")
            minutes=True
        except AttributeError:
            minutes=False    
        cook_Hour_html=soup.find(id="cookHoursSpan")
        try:
            holder=cook_Hour_html.renderContents() 
            hour_len=holder.replace("<em>","").replace("</em>","")
            hours=True
        except AttributeError:
            hours=False
        if hours==True and minutes==True:
            return "Cook Time is "+hour_len+" and "+min_len
        elif hours==False and minutes==True:
            return "Cook Time is "+min_len
        elif hours==True and minutes==False:
            return "Cook Time is "+hour_len
        else:
            return "No cook time listed"
    except:
        return "No cook time listed"
   
#This function returns a list of strings that represent each of the discrete
#direction steps in order. It also breaks up the directions so that each
#sentance is considered its own step
def get_Directions(soup):
    try:        
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
            holder=item.replace("&#34;",'"')
            if holder[0]==" ":
                holder=holder[1:len(holder)]
                sub_directions[i]=holder
            i=i+1;
        return sub_directions
    except:
        return "No directions listed"
#This function returns a list of strings that that have the number of calories,
#total cholesterol, amount of fiber, amount of sodium, total carbohydrates,
#the fat and protein
def get_Nutrition(soup):
    try:    
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
    except:
        return "No nutrients listed"

#This Function returns a string stating the number of servings
def get_Servings(soup):
    try:        
        servings_html=soup.find("span", {"itemprop" : "servingSize"})
        servings="The serving size is "+servings_html.renderContents()
        return servings
    except:
        return "No servings listed"

#This wraps the recipe information into a text file that is named after the 
#recipe name (once that name has been normalized to ensure it is a valid file
#name)
def wrap(soup,directory):
    #Getting the name of the recipe for usage to write to the file
    recipe_name=get_Name(soup)

    #turn the recipe name into a format suitable for a file name
    file_name=(recipe_name.replace(' ','').replace('/','').replace('?','')
    .replace('?','').replace('%','').replace('*','').replace(':','')
    .replace('"','').replace('<','').replace('>','').replace('.',''))
    #completeName=os.path.join(directory,file_name,".txt")
    print("Now Creating "+file_name)    
    completeName=directory+file_name+".txt"
    fo=open(completeName,'w')
    
    #Getting the info to write, and then writing the information
    description=get_Description(soup)
    ingredients=get_Ing(soup)
    prep_time=get_Prep_Time(soup)
    cook_time=get_Cook_Time(soup)
    directions=get_Directions(soup)
    nutrition=get_Nutrition(soup)
    servings=get_Servings(soup) 
    #if (type(i) is int) == True:
    if (type(recipe_name) is str) == True:
        fo.write(recipe_name)
    if (type(description) is str) == True:
        fo.write("\n")
        fo.write(description)
    if (type(servings) is str) == True:
        fo.write("\n")
        fo.write(servings)
    if (type(prep_time) is str) == True:
        fo.write("\n")
        fo.write(prep_time)
    if (type(cook_time) is str) == True:
        fo.write("\n")
        fo.write(cook_time)
    if (type(ingredients) is list) == True:
        fo.write("\nIngredients")
        for item in ingredients:
            fo.write("\n")
            fo.write(item)
    if (type(directions) is list) == True:
        fo.write("\nDirections")
        i=1
        for item in directions:
            fo.write("\n"+str(i)+") ")
            fo.write(item)
            i=i+1
    if (type(nutrition) is list) == True:
        fo.write("\nNutritional Information per Serving")
        for item in nutrition:
            fo.write("\n")
            fo.write(item)
    fo.close()
 
#More testing   
