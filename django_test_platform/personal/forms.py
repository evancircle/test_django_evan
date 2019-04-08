from django import forms
from personal.models import Project

class Projectform(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['id', 'name', 'describe', 'status']

