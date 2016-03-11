'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from operator import itemgetter
import random
from fat_transformations import *
from carbtransformations import *
import re

results = {}
recipe_book = {}

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

#move elsewhere later
tool_verb_map = {
  'chop':'knife',
  'stir':'wooden spoon',
  'beat':'fork',
  'cream':'hand mixer',
  'dice':'knife',
  'drizzle':'spoon',
  'fold':'wooden spoon',
  'glaze':'spoon',
  'julienne':'knife',
  'marinate':'bowl',
  'mince':'knife',
  'shred':'food processor',
  'sift':'colander',
  'slice':'knife',
  'peel':'peeler',
  'puree':'blender',
  'grate':'grater',
  'crush':'pestle mortar',
  'whisk':'whisk'
}

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    global results
    results = {}
    get_ingredients(soup, results)
    print '\n'
    get_directions(soup)
    get_methods(soup, results)
    get_tools(soup, results)
    get_steps(soup, results)
    # uncomment later
    #print_recipe(results)
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

    #for x in ingredients:
    #    print x

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
        if element != '':
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
        for verb in tool_verb_map:
            tool = tool_verb_map[verb]
            if directions_list[x] == verb and tool not in cnt:
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
    dct["title"] = title[:-17].lower()

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

def print_recipe(dct):
    for key in dct:
        if key != 'steps':
            print key + ":\n"
            if isinstance(dct[key], basestring):
                print dct[key]
            elif isinstance(dct[key], list):
                for value in dct[key]:
                    if isinstance(value, dict):
                        for x in value:
                            print x + ": " + str(value[x])
                        print '\n'
                    else:
                        print value
            print '\n'
        else:
            print key + ":\n"
            for index, elem in enumerate(dct[key]):
                if elem != "":
                    print str(index+1) + ". " + elem
            print '\n'

def print_transform_recipe(dct):
    for key in dct:
        if key != 'steps':
            if key != 'cooking tools' and key != 'cooking methods' and key != 'primary cooking method':
                print key + ":\n"
                if isinstance(dct[key], basestring):
                    print dct[key]
                elif isinstance(dct[key], list):
                    for value in dct[key]:
                        if isinstance(value, dict):
                            for x in value:
                                print x + ": " + str(value[x])
                            print '\n'
                        else:
                            print value
                print '\n'
        else:
            print key + ":\n"
            for index, elem in enumerate(dct[key]):
                if elem != "":
                    print str(index+1) + ". " + elem
            print '\n'


def transform(dct,transType):

    if (transType == 1):
        substitutes = {
        #proof of conept, needs refining
            'chicken':['tuna','tofu', 'salmon'],
            'steak':['tuna','tofu', 'salmon'],
            'beef':['tuna','tofu', 'salmon'],
            'turkey':['tuna','tofu', 'salmon'],
            'bacon':['tofu','tofu','tofu']
        }
    elif (transType == 2):
        substitutes = {
        #proof of conept, needs refining
            'tuna':['chicken','steak', 'turkey'],
            'salmon':['chicken','steak', 'turkey'],
            'tofu':['chicken','steak', 'turkey']
        }
    elif (transType == 3):
        substitutes = {
        #proof of conept, needs refining
            'chicken':['tofu', 'tofu','tofu'],
            'steak':['tofu', 'tofu','tofu'],
            'beef':['tofu', 'tofu','tofu'],
            'turkey':['tofu', 'tofu','tofu'],
            'bacon':['tofu', 'tofu','tofu'],
            'tuna':['tofu', 'tofu','tofu'],
            'salmon':['tofu', 'tofu','tofu'],
            'tofu':['tofu', 'tofu','tofu']
        }
    else:
        substitutes = {
        #proof of conept, needs refining
            'tofu':['chicken','steak','tuna']
        }


    transformed_recipe = dct.copy()

    choice = random.randint(0, 2)

    # Substituting ingredients into steps
    new_list = transformed_recipe['steps']
    for value in substitutes:
        new_list = [w.replace(value, substitutes[value][choice]) for w in new_list]
    transformed_recipe['steps'] = new_list

    # substituing ingredients into ingredient list
    new_ingredients = transformed_recipe['ingredients']
    subs = list(substitutes.keys())
    for dct in new_ingredients:
        for word in dct['name'].split():
            if word in subs:
                dct['name'] = substitutes[word][choice]

    new_title = transformed_recipe['title']
    for word in transformed_recipe['title'].split():
        if word in subs:
            new_title = transformed_recipe['title'].replace(word,substitutes[word][choice])
    transformed_recipe['title'] = new_title

    print_transform_recipe(transformed_recipe)

def high2lowfat(dct):

    transformed_recipe = dct.copy()
    new_ingredients = transformed_recipe['ingredients']
    new_steps = transformed_recipe['steps']
    new_title = transformed_recipe['title']

    for y in new_ingredients:
        for z in high_to_low_stopwords:
            if z in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(z, '')

            if z in y['descriptor'].lower():
                y['descriptor'] = y['descriptor'].encode('utf-8')
                y['descriptor'] = y['descriptor'].replace(z, low_to_high_stopwords[z])

    for x in substitutions:
        for y in new_ingredients:
            if y['name'] in ignorelist:
                pass
            elif x in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(x, substitutions[x])


    for z in (high_to_low_stopwords):
        if z == ',':
            pass
        else:
            for y in new_steps:
                if z in y.lower():
                    new_steps = new_steps.remove(z)

    #replacements in steps
    split_steps = []
    for y in range(0, len(new_steps)):
        split_steps.append(new_steps[y].split())


    for x in substitutions:
        for y in range(0, len(split_steps)):
            for z in range(0, len(split_steps[y])):
                if x == split_steps[y][z]:
                    split_steps[y][z] = split_steps[y][z].replace(x, substitutions[x])
                if x + ',' == split_steps[y][z]:
                    split_steps[y][z] = split_steps[y][z].replace(x, substitutions[x])
                if x + '.' == split_steps[y][z]:
                    split_steps[y][z] = split_steps[y][z].replace(x, substitutions[x])

    for y in range(0, len(split_steps)):
        split_steps[y] = " ".join(split_steps[y])

    new_steps = split_steps




    for x in method_substitutions:
        new_steps = [w.replace(x, method_substitutions[x]) for w in new_steps]


    new_title = new_title.encode('utf-8').lower()
    for x in substitutions:
        for y in ignorelist:
            if y in new_title:
                pass
            elif x in new_title.lower():
                new_title =new_title.replace(x, substitutions[x])

    for x in method_substitutions:
        if x in new_title.lower():
            new_title =new_title.replace(x, method_substitutions[x])
            print new_title

    transformed_recipe['ingredients'] = new_ingredients
    transformed_recipe['steps'] = new_steps
    transformed_recipe['title'] = new_title.upper()

    print "low fat version:"
    print_transform_recipe(transformed_recipe)


def low2highfat(dct):

    transformed_recipe = dct.copy()
    new_ingredients = transformed_recipe['ingredients']
    new_steps = transformed_recipe['steps']
    new_title = transformed_recipe['title']

    for y in new_ingredients:
        for z in low_to_high_stopwords:
            if z in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(z, low_to_high_stopwords[z])
            if z in y['descriptor'].lower():
                y['descriptor'] = y['descriptor'].encode('utf-8')
                y['descriptor'] = y['descriptor'].replace(z, low_to_high_stopwords[z])


    for x in low_to_high_subs:
        for y in new_ingredients:
            if y['name'] in ignorelist:
                pass
            elif x in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(x, low_to_high_subs[x])


    for x in substitutions:
        for y in new_ingredients:
            if substitutions[x] in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(substitutions[x], x)



    for z in low_to_high_stopwords:
        if z == ',':
            pass
        else:
            for y in new_steps:
                if z in y.lower():
                    y = y.encode('utf-8')
                    y = y.replace(low_to_high_stopwords[z], z)
                    #print new_steps


    for x in substitutions:
        new_steps = [w.replace(substitutions[x], x) for w in new_steps]




    new_title = new_title.encode('utf-8').lower()
    for x in substitutions:
         if x in new_title.lower():
             new_title =new_title.replace(x, substitutions[x])



    transformed_recipe['ingredients'] = new_ingredients
    transformed_recipe['steps'] = new_steps
    transformed_recipe['title'] = new_title

    print "high fat version:"
    print_transform_recipe(transformed_recipe)

def lowcarb(dct):
    transformed_recipe = dct.copy()
    new_ingredients = transformed_recipe['ingredients']
    new_steps = transformed_recipe['steps']
    new_title = transformed_recipe['title']

    for y in new_ingredients:
        for z in high_to_lowcarb_stopwords:
            if z in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(z, '')

            if z in y['descriptor'].lower():
                y['descriptor'] = y['descriptor'].encode('utf-8')
                y['descriptor'] = y['descriptor'].replace(z, '')

    for x in carbsubstitutions:
        for y in new_ingredients:
            if x in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(x, carbsubstitutions[x])


    for z in high_to_lowcarb_stopwords:
        if z == ',':
            pass
        else:
            for y in new_steps:
                if z in y.lower():
                    new_steps = new_steps.remove(z)


    for x in carbsubstitutions:
        new_steps = [w.replace(x, carbsubstitutions[x]) for w in new_steps]



    new_title = new_title.encode('utf-8').lower()

    for x in carbsubstitutions:
         if x in new_title.lower():
             new_title =new_title.replace(x, carbsubstitutions[x])

    new_title = new_title + "(low carb)"



    transformed_recipe['ingredients'] = new_ingredients
    transformed_recipe['steps'] = new_steps
    transformed_recipe['title'] = new_title

    print "low carb version:"
    print_transform_recipe(transformed_recipe)

def highcarb(dct):
    transformed_recipe = dct.copy()
    new_ingredients = transformed_recipe['ingredients']
    new_steps = transformed_recipe['steps']
    new_title = transformed_recipe['title']

    for y in new_ingredients:
        for z in low_to_highcarb_stopwords:
            if z in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(z, '')

            if z in y['descriptor'].lower():
                y['descriptor'] = y['descriptor'].encode('utf-8')
                y['descriptor'] = y['descriptor'].replace(z, '')


    for x in low_to_highcarb_subs:
        for y in new_ingredients:
            if x in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(x, low_to_highcarb_subs[x])


    for x in carbsubstitutions:
        for y in new_ingredients:
            if carbsubstitutions[x] in y['name'].lower():
                y['name'] = y['name'].encode('utf-8')
                y['name'] = y['name'].replace(carbsubstitutions[x], x)



    for z in low_to_highcarb_stopwords:
        if z == ',':
            pass
        else:
            for y in new_steps:
                if z in y.lower():
                    y = y.encode('utf-8')
                    y = y.remove(z)


    for x in carbsubstitutions:
        new_steps = [w.replace(carbsubstitutions[x], x) for w in new_steps]

    new_title = new_title.encode('utf-8').lower()
    for x in carbsubstitutions:
         if x in new_title.lower():
             new_title =new_title.replace(x, carbsubstitutions[x])

    transformed_recipe['ingredients'] = new_ingredients
    transformed_recipe['steps'] = new_steps
    transformed_recipe['title'] = new_title

    print "high carb version:"
    print_transform_recipe(transformed_recipe)



def main():
    '''This is our main function!'''
    #intialize all our txt file lists
    pre_parse()

    # http://allrecipes.com/recipe/18866/canadian-bacon-macaroni-and-cheese/

    global recipe_book
    recipe_book[len(recipe_book.keys())] = autograder('http://allrecipes.com/recipe/18866/canadian-bacon-macaroni-and-cheese/')

    while True:
        print '\n'
        print "\noptions:\n1. enter recipe (via url)\n2. transform an existing recipe\n"
        user_input = input("choose a function: ")
        if (user_input == 1):
            url = str(raw_input("enter recipe url: "))
            recipe_book[len(recipe_book.keys())] = autograder(url)
        elif (user_input == 2):
            if len(recipe_book.keys()) != 0:
                for key in recipe_book:
                    print str(key) + " : " + recipe_book[key]['title']
                choice = input("which recipe: ")
                print "\noptions:\n1. to pescatarian\n2. from pescatarian\n3. low fat\n4. high fat\n5. low carb\n6. high carb\n7. to vegetarian\n8. from vegetarian\n"
                choice2 = input("which transform: ")
                if (choice2 == 1):
                    transform(recipe_book[choice],1)
                elif (choice2 == 2):
                    transform(recipe_book[choice],2)
                elif (choice2 == 3):
                    high2lowfat(recipe_book[choice])
                elif (choice2 == 4):
                    low2highfat(recipe_book[choice])
                elif (choice2 == 5):
                    lowcarb(recipe_book[choice])
                elif (choice2 == 6):
                    highcarb(recipe_book[choice])
                elif (choice2 == 7):
                    transform(recipe_book[choice],3)
                elif (choice2 == 8):
                    transform(recipe_book[choice],4)
                else:
                    print "invalid choice"
            else:
                print "you must upload a recipe first"

        else:
            print "invalid choice\n"

    print '\n'
    return


if __name__ == '__main__':
    main()
