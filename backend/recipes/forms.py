from django import forms

from .models import Recipe


class RecipeAdminForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'name', 'cooking_time', 'author',
            'tags', 'text', 'image', 'ingredients'
        )

    def clean_igredients(self):
        [print(i) for i in self.data]
        print('!!.!!!!!!!!!')
        return self.cleaned_data['ingredients']
