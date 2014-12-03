Cookie_Monster
==============

Has an insatiable appetite for recipes!

These two scripts allow you to scrape allrecipes.com's rankings of their recipes, and returns a text file of the recipe ingredients. The user can set up what directory they want to use and then choose the range of pages they want to search (or grab all 54,000 recipes). Nominally to get all the recipes the crawler starts at the top page of the listing of highest ranked recipes, and then continues until it runs out of pages. The following information is put into a text file for each recipe:
Recipe Name
Recipe Description
Serving Size
Prep Time
Cooking Time
Ingredients
Directions
Nutritional Information

To use this grab the two files, make sure you have beautiful soup, and then run fruitfly. Spatula is the generic scraper, while fruitfly is the crawler which uses spatula. Spatula has generic functions for scraping individual elements if you give it a soup object, and it also as a function which will wrap all the information up into a new .txt file
