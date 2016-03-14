EECS 337 PROJECT 2

GROUP 4: Eric Brownrout, Sonia Nigam, Shraya Soundararajan, Richard Gates Porter

PROJECT DESCRIPTION:
Our project takes a user-inputted url from allrecipes.com, and returns parsed information as well as options to transform the given recipe.  We leverage mapping, stopwords, and randomization in order to effectively substitute ingredients and produce a transformed versions of the recipe (to/from pescatarian, to/from vegetarian, high/low carb, high/low fat, indian, italian, chinese)

REQUIRED FUNCTIONS
- parse_ingredient(): name, quantity, measurement
- get_tools()
- get_methods(): primary method
- transform(): to/from pescatarian and to/from vegetarian
- high2lowfat(): to low fat
- low2highfat() : to high fat
- lowcarb(): to low carb
- highcarb(): to high carb
- indian: to indian-style cuisine
- italian: to italian-style cuisine

OPTIONALS
- parse_ingredient(): descriptor, preparation
- get_methods(): other cooking methods used
- get_structuredsteps(); steps
- chinese(): to chinese-style cuisine

* also implemented a recipe book for storage, and the ability to stack transformations *

EXTERNAL LIBRARIES: 

- beautifulsoup: accept a url and programmatically fetch the page, and then parse tools, ingredients, methods, directions, and steps.

- nltk corpus: we leveraged tokenization to iterate through strings and identify words for substitution

REPOSITORIES
The structure behind our cuisine transformations and how to map verb actions to tools was inspired by this repo: https://github.com/jeanniet13/Recipes
