from django import forms
from .models import Product,ProductImage
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput()
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image','in_stock']
        

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'color'] 
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    
class EditProfileForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
