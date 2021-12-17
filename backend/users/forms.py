from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import MyUser


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MyUser
        fields = ('username', 'email')


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = MyUser

        # fields = (
        #    ('username', 'email', ),
        #    ('first_name', 'last_name', ),
        #    ('avatar', )
        # )
