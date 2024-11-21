from django import forms
from .models import ExcelFile

class ExcelFileForm(forms.ModelForm):
    file = forms.FileField()
    offset = forms.IntegerField(initial=0)
    limit = forms.IntegerField(initial=1000)