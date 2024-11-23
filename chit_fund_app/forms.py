# chit_fund_app/forms.py
from django import forms

class DateForm(forms.Form):
    specific_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Select a Date"
    )
