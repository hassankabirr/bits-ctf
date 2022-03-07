from django.forms import ModelForm
from .models import Question, Team
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class FlagForm(forms.Form):
    flag = forms.CharField(label='Flag', max_length=255, widget=forms.TextInput(attrs={'type': "text", 'id': "flag", 'class': "input", 'placeholder': "پرچم"}))


class JoinTeamForm(forms.Form):
    error_dic = {
        'invalid': 'Enter a valid value'
    }
    token = forms.UUIDField(label='Please Enter Your Group Token:', error_messages=error_dic,
                            widget=forms.TextInput(attrs={'type': "text", 'class': "input", 'placeholder': "کد ورود به تیم"}))


class CreateTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'type': "text", 'class': "input", 'placeholder': "نام تیم "})


class UserCreation(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email', 'university', 'password1', 'password2']
        labels = {
            'first_name': "Name"
        }
    def __init__(self, *args, **kwargs):
        super(UserCreation, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'username':
                field.widget.attrs.update({'type': 'text', 'placeholder': "نام کاربری"})
            elif name == 'first_name':
                field.widget.attrs.update({'type': 'text', 'placeholder': "نام و نام خانوادگی "})
            elif name == 'email':
                field.widget.attrs.update({'type': 'text', 'placeholder': "ایمیل"})
            elif name == 'university':
                field.widget.attrs.update({'type': 'text', 'placeholder': "نام مدرسه / دانشگاه"})
            elif name == 'password1':
                field.widget.attrs.update({'type': 'password', 'placeholder': "رمز عبور"})
            elif name == 'password2':
                field.widget.attrs.update({'type': 'password', 'placeholder': "رمز عبور مجدد"})
            field.widget.attrs.update({'class': 'input'})