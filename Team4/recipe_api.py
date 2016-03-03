'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from operator import itemgetter

answers = {}

equivalents = {
    't': 'teaspoon',
    'tsp':'teaspoon',
    'tbsp':'tablespoon',
    'c':'cup',
    'oz':'ounce',
    'pt': 'pint',
    'qt': 'quart',
    'gal':'gallon',
    'lb':'pound'
}

units = []
descriptors = []
tools = []
methods = []
preparations = []

decrement_check = {"mixing bowl": "mix", "baking pan": "bake", "baking soda": "bake", "baking powder":"bake"}

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

    text_file = open("Team4/preparations.txt", "r")
    lines = text_file.readlines()
    global preparations
    for x in lines:
        new = x.rstrip('\n')
        preparations.append(new)

def get_ingredients(soup, dct):
    dct["ingredients"] = []
    letters = soup.find_all("span", itemprop="ingredients")
    
    for element in letters:
        quantity, measurement, name, descriptor, preparation = parse_ingredient(element.get_text().lower())
        d = {
          'name': name,
          'quantity':quantity,
          'measurement':measurement,
          'descriptor': descriptor,
          'preparation':  preparation,
          'prep-description': "none"
        }
        dct["ingredients"].append(d)
    
    # for x in dct['ingredients']:
    #     for k,v in x.items():
    #         print k + " : " + v

def parse_ingredient(ingredient):
    
    quantity = ''
    name = ''
    measurement = '' 
    descriptor = ''
    preparation = ''

    global equivalents
    synonyms = []
    
    global units
    global descriptors

    for key in equivalents:
        synonyms.append(key)

    ingLst = ingredient.split()
    for word in ingLst: 
        if word in synonyms:
            word = equivalents[word]
        if word[0].isnumeric():
            quantity = word
            continue
        elif word in units:
            measurement = word
            continue
        elif word in descriptors:
            descriptor = word
            continue
        elif word in preparations:
            preparation = word
            continue
    
    if measurement in ingLst:
        ingLst.remove(measurement)
    if quantity in ingLst:
        ingLst.remove(quantity)
    if descriptor in ingLst:
        ingLst.remove(descriptor)
    if preparation in ingLst:
        ingLst.remove(preparation)

    name = ' '.join(ingLst)

    if quantity == '':
        quantity = 'none'
    else:
        quantity = convert(quantity)
    if measurement == '':
        measurement = 'none'
    if descriptor == '':
        descriptor = 'none'
    if preparation == '':
        preparation = 'none'

    return quantity, measurement, name, descriptor, preparation

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

def get_steps(soup,dct):
    dct['steps'] = []
    directions = soup.find_all("span", class_="recipe-directions__list--item")
    for element in directions:
        dct['steps'].append(str(element.text).lower())
    return

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

def get_methods(soup, dct):
    cnt = Counter()
    tokenizer = RegexpTokenizer(r'\w+')
    dct["cooking methods"] = []
    dct["primary cooking method"] = " "
    
    title = soup.title.text
    title_string = tokenizer.tokenize(title)
    dct["title"] = title[:-17]

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
            elif y + "ed" == x.lower():
                cnt[y] += 1
            elif y[:-1]+ "ing" == x.lower():
                cnt[y]+=1


    #decrement tools mistaken for methods

    for x in range(0, len(directions_list)-1):
        for y in decrement_check:
            test_string = directions_list[x] + " " + directions_list[x+1]
            if test_string == y:
                cnt[decrement_check[y]] -= 1


    flag = True
    if flag:
        for x in title_string:
            for y in methods:
                if y == x.lower():
                    dct["primary cooking method"] = y
                    flag = False
                elif y + "ed" == x.lower():
                    dct["primary cooking method"] = y
                    flag = False
                elif y + "d" == x.lower():
                    dct["primary cooking method"] = y
                    flag = False

    if flag:
        max_list = []
        max_cnt = cnt.most_common(1)[0][1]
        
        for x,v in cnt.most_common():
            if v== max_cnt:
                max_list.append(x)

        max_list.sort()

        dct["primary cooking method"] = max_list[0]

    for x in cnt.most_common():
        dct["cooking methods"].append(x[0])

def main():
    '''This is our main function!'''
    r = urllib.urlopen('http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/').read()
    soup = BeautifulSoup(r, "lxml")

    #intialize all our txt file lists
    pre_parse()

    global answers
    answers = {}
    get_ingredients(soup, answers)
    print '\n'
    get_directions(soup)
    get_methods(soup, answers)
    get_tools(soup, answers)
    get_steps(soup, answers)
    
    for key in answers:
        print key + ":\n"
        #if hasattr(answers[key], 'lower'):
        if isinstance(answers[key], basestring):
            print answers[key]
        elif isinstance(answers[key], list):
            for value in answers[key]:
                if isinstance(value, dict):
                        for x in value:
                            print x + ": " + str(value[x])
                        print '\n'
                else:
                    print value
        print '\n'
    return


if __name__ == '__main__':
    main()
