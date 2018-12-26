from django import forms

class MailForm(forms.Form):
    email_destination = forms.CharField(label='Email destination', max_length=100)
    email_content = forms.CharField(label='Email content')
