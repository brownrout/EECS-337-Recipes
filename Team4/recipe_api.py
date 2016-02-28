'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def autograder(url):
    '''Accepts the URL for a recipe, and returns a dictionary of the
    parsed results in the correct format. See project sheet for
    details on correct format.'''
    # your code here
    return results


def main():
    '''This is our main function!'''
    r = urllib.urlopen('http://allrecipes.com/recipe/220414/hot-tamale-pie/').read()
    soup = BeautifulSoup(r)
    print soup.prettify()[0:2000]
    return

if __name__ == '__main__':
    main()