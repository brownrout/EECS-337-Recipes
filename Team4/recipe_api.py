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
    for element in letters:
        print element.get_text()

def get_directions(soup):
    directions_string = ""
    directions = soup.find_all("span", class_="recipe-directions__list--item")
    for element in directions:
        #print str(element.text)
        directions_string += " " + str(element.text)
    return directions_string

def get_tools(soup):
    cnt = Counter()
    tokenizer = RegexpTokenizer(r'\w+')

    directions_string = get_directions(soup)
    text_file = open("Team4/tools.txt", "r")
    lines = text_file.readlines()
    tools = []
    for x in lines:
        new = x.rstrip('\n')
        tools.append(new)

    directions_list = map(lambda x:x.lower(),tokenizer.tokenize(directions_string))

    used_list = []
    for x in range(len(directions_list)):
        if x + 1 < len(directions_list):
            two_word_tool = directions_list[x] + ' ' + directions_list[x+1]
            used_word = directions_list[x+1]
        one_word_tool = directions_list[x]
        for tool in tools:
            if tool == two_word_tool:
                used_list.append(used_word)
                cnt[tool] += 1
            elif tool == one_word_tool and tool not in used_list:
                cnt[tool] +=1

    print "all of the tools are:"
    for x in cnt.most_common():
        print x[0]

def get_methods(soup):
    cnt = Counter()
    tokenizer = RegexpTokenizer(r'\w+')

    directions_string = get_directions(soup)
    #print directions_string
    text_file = open("Team4/methods.txt", "r")
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
                cnt[y] += 1
            elif y + "s" == x.lower():
                cnt[y+"s"] += 1
                cnt[y]+=1
            elif y + "er" == x.lower():
                cnt[y+"er"] += 1
                cnt[y] += 1
            elif y[:-1]+ "ing" == x.lower():
                cnt[y[:-1]+ "ing"] += 1
                cnt[y]+=1
    #print cnt
    print "the most common method: " + cnt.most_common(1)[0][0]
    print "all of the methods are:"
    for x in cnt.most_common():
        print x[0]



def main():
    '''This is our main function!'''
    r = urllib.urlopen('http://allrecipes.com/recipe/80827/easy-garlic-broiled-chicken/').read()
    soup = BeautifulSoup(r, "lxml")
    get_ingredients(soup)
    print '\n'
    get_directions(soup)
    get_methods(soup)
    get_tools(soup)

    return


if __name__ == '__main__':
    main()
