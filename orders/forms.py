from django import forms
from django.utils.html import strip_tags


class OrderForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Email',
            'readonly': 'readonly'
        })
    )
    company = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Company (optional)'
        })
    )
    address1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black pr-10',
            'placeholder': 'Address Line 1'
        })
    )
    address2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Address Line 2 (optional)'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'City'
        })
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Country'
        })
    )
    province = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'State/Province'
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Postal Code'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black pr-10',
            'placeholder': 'Phone (optional)'
        })
    )


    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            user_fields = ['first_name', 'last_name', 'email', 'company',
                           'address1', 'address2', 'city', 'country',
                           'province', 'postal_code', 'phone']
            for field in user_fields:
                if field in self.fields:
                    self.fields[field].initial = getattr(user, field, None)


    def clean(self):
        cleaned_data = super().clean()
        for field in ['company', 'address1', 'address2', 'city', 
                      'country', 'province', 'postal_code', 'phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
    