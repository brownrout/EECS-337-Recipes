'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib
from collections import Counter
from nltk.tokenize import RegexpTokenizer
answers = {}

units = []
descriptors = []
tools = []
methods = []


def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    # your code here
    return results

def pre_parse():
    text_file = open("Team4/units.txt", "r")
    lines = text_file.readlines()
    global units
    for x in lines:
        new = x.rstrip('\n')
        units.append(unicode(new, 'utf-8'))

    text_file = open("Team4/descriptor.txt", "r")
    lines = text_file.readlines()
    global descriptors
    for x in lines:
        new = x.rstrip('\n')
        descriptors.append(unicode(new, 'utf-8'))

    text_file = open("Team4/tools.txt", "r")
    lines = text_file.readlines()
    global tools
    for x in lines:
        new = x.rstrip('\n')
        tools.append(new)

    text_file = open("Team4/methods.txt", "r")
    lines = text_file.readlines()
    global methods
    for x in lines:
        new = x.rstrip('\n')
        methods.append(new)

def get_ingredients(soup, dct):
    dct["ingredients"] = []
    letters = soup.find_all("span", itemprop="ingredients")
    
    for element in letters:
        quantity, measurement, name, descriptor = parse_ingredient(element.get_text().lower())
        d = {
          'name': name,
          'quantity':quantity,
          'measurement':measurement,
          'descriptor': descriptor,
          'preparation':  "unimplemented",
          'prep-description': "unimplemented"
        }
        dct["ingredients"].append(d)
    
    # for x in dct['ingredients']:
    #     for k,v in x.items():
    #         print k + " : " + v
    print dct['ingredients']

def parse_ingredient(ingredient):
    
    quantity = ''
    name = ''
    measurement = '' 
    descriptor = ''
    
    global units
    global descriptors

    ingLst = ingredient.split()
    for word in ingLst:
        if word[0].isnumeric():
            quantity = word
            continue
        elif word in units:
            measurement = word
            continue
        elif word in descriptors:
            descriptor += word
            continue
    
    if measurement in ingLst:
        ingLst.remove(measurement)
    if quantity in ingLst:
        ingLst.remove(quantity)
    if descriptor in ingLst:
        ingLst.remove(descriptor)

    name = ' '.join(ingLst)

    if quantity == '':
        quantity = 'none'
    else:
        quantity = convert(quantity)
    if measurement == '':
        measurement = 'none'
    if descriptor == '':
        descriptor = 'none'

    return quantity, measurement, name, descriptor

# http://stackoverflow.com/questions/575925/how-to-convert-rational-and-decimal-number-strings-to-floats-in-python
def convert(s):
    try:
        float(s)
        return s
    except ValueError:
        num, denom = s.split('/')
        return float(num) / float(denom)


def get_directions(soup):
    directions_string = ""
    directions = soup.find_all("span", class_="recipe-directions__list--item")
    for element in directions:
        #print str(element.text)
        directions_string += " " + str(element.text)
    return directions_string

def get_tools(soup, dct):
    cnt = Counter()
    dct["cooking tools"] = []

    tokenizer = RegexpTokenizer(r'\w+')

    directions_string = get_directions(soup)

    global tools

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

    for x in cnt.most_common():
        dct["cooking tools"].append(x[0])

    print dct

def get_methods(soup, dct):
    cnt = Counter()
    tokenizer = RegexpTokenizer(r'\w+')
    dct["cooking methods"] = []
    dct["primary cooking method"] = " "

    directions_string = get_directions(soup)
    #print directions_string

    global methods

    directions_list = tokenizer.tokenize(directions_string)

    for x in directions_list:
        for y in methods:
            if y == x.lower():
                cnt[y] += 1
            elif y + "ing" == x.lower():
                cnt[y] += 1
            elif y + "s" == x.lower():
                cnt[y]+=1
            elif y + "er" == x.lower():
                cnt[y] += 1
            elif y[:-1]+ "ing" == x.lower():
                cnt[y]+=1
    dct["primary cooking method"] = cnt.most_common(1)[0][0]
    for x in cnt.most_common():
        dct["cooking methods"].append(x[0])



def main():
    '''This is our main function!'''
    r = urllib.urlopen('http://allrecipes.com/recipe/80827/easy-garlic-broiled-chicken/').read()
    soup = BeautifulSoup(r, "lxml")

    #intialize all our txt file lists
    pre_parse()

    answers = {}
    get_ingredients(soup, answers)
    print '\n'
    get_directions(soup)
    get_methods(soup, answers)
    get_tools(soup, answers)

    return


if __name__ == '__main__':
    main()
