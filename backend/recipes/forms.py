from django.forms import ModelForm
from django.forms.widgets import TextInput
from recipes.models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
