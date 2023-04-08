from django import forms
from django.core import validators


class AskForm(forms.Form):
    place = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")], required=True)
    duration = forms.IntegerField(validators=[validators.MinValueValidator(2, "Please plan for atleast 2 or more days")], required=True)

from django.forms import ModelForm
from .models import Queries, Food

# Create the form class.
class QForm(ModelForm):
    class Meta:
        model = Queries
        # fields = '__all__'
        fields = ['place', 'duration']
        widgets = {
            'place':forms.TextInput(attrs={'class':"form-control", 'placeholder':"Destination",'id':'place_id', 'type':'text'}),
            'duration':forms.NumberInput(attrs={'class':"form-control", 'placeholder':"No.of Days",'id':'duration_id', 'type':'number', 'onkeypress':"return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))"}),
        }

class FForm(ModelForm):
    class Meta:
        model = Food
        # fields = '__all__'
        fields = ['gpt_place']
        widgets = {
            'gpt_place':forms.TextInput(attrs={'class':"form-control", 'placeholder':"Destination",'id':'food_place_id', 'type':'text'}),

        }

# class PersonalizedForm(ModelForm):
#     class Meta:
#         model = Queries
#         fields = '__all__'
#         widgets = {
#             'place':forms.TextInput(attrs={'class':"form-control", 'placeholder':"Destination",'id':'place_id', 'type':'text'}),
#             'duration':forms.NumberInput(attrs={'class':"form-control", 'placeholder':"No.of Days",'id':'duration_id', 'type':'number', 'onkeypress':"return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))"}),
#             'personalize':forms.TextInput(attrs={'class':"form-control", 'placeholder':"for example: make it religious, adventure trip",'id':'personalize_id', 'type':'text'}),
#         }