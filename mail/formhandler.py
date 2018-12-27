from django import forms

class MailForm(forms.Form):
    destination = forms.EmailField(label='To')
    subject = forms.CharField(label='Subject')
    content = forms.CharField(label='Content', widget=forms.Textarea)
    send_type = forms.ChoiceField(
            choices = (
                ('individual', 'Send individually'),
                ('bcc', 'Send as BCC')
            )
        )
    send_list = forms.FileField(label='Upload CSV')

    def clean(self):
        return self.cleaned_data
