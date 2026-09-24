from django import forms
from users.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'country', 'u_age', 'pincode', 'city', 'passwords']
        labels = {
            'user_id': 'User ID',
            'user_name': 'User Name',
            'country': 'Country',
            'u_age': 'User age',
            'pincode': 'pincode',
            'city': 'City',
            'passwords': 'Passwords',
        }
        widgets = {
            'user_id': forms.TextInput(attrs={'placeholder': 'Enter user ID'}),
            'user_name': forms.TextInput(attrs={'placeholder': 'Enter user Name'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter country'}),
            'u_age': forms.TextInput(attrs={'placeholder': 'Enter Your age'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter pincode'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city'}),
            'passwords': forms.TextInput(attrs={'placeholder': 'Enter passwords'}),
        }

    def clean_u_age(self):
        age = self.cleaned_data.get('u_age')
        if age is not None and age <= 0:
            raise forms.ValidationError("User age must be greater than 0.")
        return age
