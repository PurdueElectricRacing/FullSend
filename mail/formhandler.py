from django import forms

class MailForm(forms.Form):
    send_list = forms.FileField(label='Upload CSV')
    subject = forms.CharField(label='Subject')
    content = forms.CharField(label='Content', widget=forms.Textarea)
    send_type = forms.ChoiceField(
            choices = (
                ('individual', 'Send individually'),
                ('bcc', 'Send as BCC')
            )
        )

    def format(self):
        cleaned = self.cleaned_data
        cleaned['send_list'] = self.parseCSV(cleaned['send_list'])
        return cleaned

    def parseCSV(self, csv_file):
        raw_csv = csv_file.read().decode('utf-8-sig')
        lines = raw_csv.splitlines()
        obj = {}
        headers = lines[0].split(',')
        for header in headers:
            obj[header] = []
        for line in lines[1:]:
            for index, item in enumerate(line.split(',')):
                obj[headers[index]].append(item)
        return obj

    def file_is_valid(self, file):
        return file['send_list'].name.endswith('.csv')
