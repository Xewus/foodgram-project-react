from os import name
from django.test import TestCase

#from termcolor import colored as clr, cprint

from  ..recipes import models
models_attrs = {
    models.Tag: (
        'name', 'colour', 'slug'
    ),
    models.Ingredient: (
        'name', 'count', 'measure'
    ),
    models.Recipe: (
        'author', 'title', 'image', 'description', 'ingredients'
    ),
}

TAG_NAME_1 =  'Test tag 1'
TAG_NAME_2 =  'Test tag 2'
TAG_COLOUR_1 = '0AF'
TAG_COLOUR_2 = 'C'
TAG_SLUG_1 = 'Test_tag_slug_1'
TAG_SLUG_2 = 'Test_tag_slug_2'


class ModelTests(TestCase):
    '''Check model "Tag"'''
    
    def test_model_attrs(self):
        for mdl, attrs in models_attrs.items():
            with self.subTest(mdl=mdl):
                print(mdl.__dir__)
