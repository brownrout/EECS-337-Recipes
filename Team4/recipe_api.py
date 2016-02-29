'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib
from collections import Counter
from nltk.tokenize import RegexpTokenizer


def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    # your code here
    return results

def get_ingredients(soup):
	letters = soup.find_all("span", itemprop="ingredients")
    #for element in letters:
        #print element.get_text()

def get_directions(soup):
    directions_string = ""
    directions = soup.find_all("span", class_="recipe-directions__list--item")
    for element in directions:
        directions_string += " " + str(element.text)
    return directions_string

def get_methods(soup):
    cnt = Counter()
    tokenizer = RegexpTokenizer(r'\w+')

    directions_string = get_directions(soup)
    print directions_string
    text_file = open("methods.txt", "r")
    lines = text_file.readlines()
    methods = []
    for x in lines:
        new = x.rstrip('\n')
        methods.append(new)

    directions_list = tokenizer.tokenize(directions_string)



    for x in directions_list:
        for y in methods:
            if y == x.lower():
                cnt[y] += 1
            elif y + "ing" == x.lower():
                cnt[y+"ing"] += 1
            elif y + "s" == x.lower():
                cnt[y+"s"] += 1
            elif y[:-1]+ "ing" == x.lower():
                cnt[y[:-1]+ "ing"] += 1
    print cnt
    print "the most common method: " + cnt.most_common(1)[0][0]
    print "all of the methods are:"
    for x in cnt.most_common():
        print x[0]



def main():
    '''This is our main function!'''
    r = urllib.urlopen('http://allrecipes.com/recipe/80827/easy-garlic-broiled-chicken/').read()
    soup = BeautifulSoup(r, "lxml")
    get_ingredients(soup)
    get_directions(soup)
    get_methods(soup)
    return


if __name__ == '__main__':
    main()