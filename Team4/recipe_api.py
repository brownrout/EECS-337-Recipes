'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    # your code here
    return results

def get_ingredients(soup):
	letters = soup.find_all("span", itemprop="ingredients")
	for element in letters:
		print element.get_text()

def main():
    '''This is our main function!'''
    r = urllib.urlopen('http://allrecipes.com/recipe/220414/hot-tamale-pie/').read()
    soup = BeautifulSoup(r, "lxml")
    get_ingredients(soup)
    return

if __name__ == '__main__':
    main()