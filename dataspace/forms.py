from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='关键字', max_length=100)
