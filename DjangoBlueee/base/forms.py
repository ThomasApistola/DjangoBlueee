from django import forms
from .models import  Profile, Medicine, Collection
 
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'date_of_birth', 'bio')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
 
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ('name', 'manufacturer', 'cures', 'sideEffects')
 
class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['medicine', 'user', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }