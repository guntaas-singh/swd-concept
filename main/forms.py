from django import forms

class complaint(forms.Form):
    complaint = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':6, 'style':"width:100%;", 'placeholder':"Please type your complain/report in this box.\n\nYour report will be mailed to Associate Dean SWD directly, and anonymously.\nIf you do not wish to be anonymous, include your Name/IDNO in the report itself."}))
