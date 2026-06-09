from django import forms
from .models import Handle, Idea, Theme, TEAM_CHOICES


class HandleForm(forms.Form):
    name = forms.CharField(max_length=50, label='Handle')
    team = forms.ChoiceField(choices=TEAM_CHOICES, widget=forms.RadioSelect, label='Team')


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Share a game idea...',
                'maxlength': 300,
            })
        }


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Suggest a theme...'})
        }
