from django import forms

class UpdateCashOutForm(forms.Form):
    cash_out = forms.IntegerField(label='Cash Out', min_value=0)
