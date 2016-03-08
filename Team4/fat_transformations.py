substitutions = {
    'unhealthy':'healthy',
    'ground beef':'lean ground turkey',
    'bacon':'canadian bacon',
    'sausage':'lean ham',
    'chicken':'skinless chicken',
    'thigh': 'breast',
    'turkey':'skinless turkey',
    'duck':'skinless turkey',
    'goose':'skinless turkey',
    'beef' :'beef loin',
    'beef chuck':'beef loin',
    'beef rib':'beef loin',
    'beef brisket':'beef loin',
    'pork spareribs':'pork tenderloin',
    'chorizo sausage':'turkey sausage',
    'milk':'skim milk',
    'cream':'evaporated skim milk',
    'iceberg lettuce':'arugula',
    'butter':'cooking spray',
    'margarine':'olive oil',
    'cheddar cheese': "low-fat cheddar cheese",
    'mozzerella cheese': "low-fat mozzerella cheese",
    'american cheese': "low-fat american cheese",
    'cottage cheese': 'low-fat cottage cheese',
    'vegetable oil':'olive oil',
    'shortening':'fat-free margarine',
    'soy sauce':'low-sodium soy sauce',
    'alfredo':'marinara',
    'pasta':'whole wheat pasta',
    'sour cream':'Greek yogurt',
    'bread':'pita',
    'flour tortilla':'corn tortilla',
    'white bread':'whole wheat bread',
    'bread' : 'whole wheat bread',
    'mayonnaise':'Greek yogurt',
    'eggs':'egg whites',
    'cream cheese':'fat-free ricotta cheese',
    'white rice':'brown rice', 
    'salted' : 'unsalted'
}


low_to_high_subs = {
    'skim milk':'whole milk',
    'low-fat milk' : "whole milk",
    'low fat milk' : 'whole milk',
    'milk' :'whole milk',
    'wheat bread' : 'white bread',
    'bread' : 'white bread'
}

low_to_high_stopwords = {"whole wheat": "", "wheat": "", "low-fat": "", "low fat": "", "healthy": "", "1%": "", '2%': "", ',': "", "canadian-style": "canadian"}
high_to_low_stopwords = ["whole", "full-fat", "1%", '2%', ',', 'with skin']


method_substitutions = {
    'deep-fryer': 'oven',
    'fryer': 'oven',
    'fry':'bake',
    'fried': 'baked',
    'frying pan': 'oven',
    'boil':'steam',
    'deep-fry':'bake',
    'pan fry':'bake'
}