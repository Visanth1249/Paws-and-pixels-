from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import UserRegistration

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserRegistration
        fields = ['username', 'email', 'password']

    def clean_repassword(self):
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword")
        if password != repassword:
            raise forms.ValidationError("Passwords do not match")
        return repassword


from django import forms
from .models import Accessory

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'description', 'price', 'image', 'quantity']  # Added quantity field
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'price': forms.NumberInput(attrs={'step': 0.01}),
            'quantity': forms.NumberInput(attrs={'min': 0}),  # Ensure non-negative quantity
        }

from django import forms
from .models import Adoption

class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = ['animal_name', 'breed', 'description', 'available', 'animal_type', 'image']  # Fields to display in the form
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'available': forms.CheckboxInput(),
            'animal_type': forms.Select(choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Bird', 'Bird')]),
        }

