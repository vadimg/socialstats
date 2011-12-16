from django import forms

class AddEventForm(forms.Form):
    event_url = forms.CharField()
