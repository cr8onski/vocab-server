from django import forms
from django.forms.formsets import BaseFormSet
from .models import Vocabulary

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, label='Name')
    email = forms.EmailField(max_length=200, label='Email')
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label='Password Again',
                                widget=forms.PasswordInput(render_value=False))

    def clean(self):
        cleaned = super(RegisterForm, self).clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password2")
        if p1 and p2:
            if p1 == p2:
                return cleaned
        raise forms.ValidationError("Passwords did not match")

class ContactForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class SearchForm(forms.Form):
    search_term = forms.CharField(label='Search:', max_length=40)

class IRIForm(forms.Form):
    vocabulary = forms.CharField(label='Vocabulary/Profile', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Vocabulary/Profile', 'class': 'form-control'}))
    termType = forms.ChoiceField(label='Term Type', required=False, choices=((None, ''), ('verbs', 'Verbs'), ('activityTypes', 'Activity Types'), ('attachments', 'Attachments'), ('extensions', 'Extensions')), widget=forms.Select(attrs={'class': 'form-control'}))
    term = forms.CharField(label='Term', required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Term', 'class': 'form-control'}))

    def clean(self):
        cleaned = super(IRIForm, self).clean()
        term_type = cleaned.get("termType", None)
        term = cleaned.get("term", None)
        if term and not term_type:
            raise forms.ValidationError("Must have a term type if giving a term")
        return cleaned

class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class VocabularyForm(forms.ModelForm):
    # vocabName = forms.CharField(label='Vocabulary Name', max_length=100)
    # vocabIRI = forms.URLField(label='Vocabulary IRI', max_length=100)
    class Meta:
        model = Vocabulary
        # fields = '__all__'
        exclude = ['user']
