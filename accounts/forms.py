'''from django import forms
from django.conf import settings
from django.db import transaction

from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICE


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class UserRegistrationForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all()
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(max_length=15)
    citizenship_id = forms.CharField(max_length=50, label="Citizenship / ID Number")
    occupation = forms.CharField(max_length=100)
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'account_type',
            'gender',
            'birth_date',
            'phone_number',
            'citizenship_id',
            'occupation',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Only check for existing users if this is a new registration (no instance yet)
        if email and not self.instance.pk:
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email.lower() if email else email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match.")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters.")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            phone_number = self.cleaned_data.get('phone_number')
            citizenship_id = self.cleaned_data.get('citizenship_id')
            occupation = self.cleaned_data.get('occupation')

            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                phone_number=phone_number,
                citizenship_id=citizenship_id,
                occupation=occupation,
                account_type=account_type,
                account_no=(
                    user.id +
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user '''
from django import forms
from django.conf import settings
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICE


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class UserRegistrationForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all()
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(max_length=15)
    citizenship_id = forms.CharField(max_length=50, label="Citizenship / ID Number")
    occupation = forms.CharField(max_length=100)
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'account_type',
            'gender',
            'birth_date',
            'phone_number',
            'citizenship_id',
            'occupation',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not self.instance.pk:
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email.lower() if email else email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match.")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters.")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            phone_number = self.cleaned_data.get('phone_number')
            citizenship_id = self.cleaned_data.get('citizenship_id')
            occupation = self.cleaned_data.get('occupation')

            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                phone_number=phone_number,
                citizenship_id=citizenship_id,
                occupation=occupation,
                account_type=account_type,
                account_no=(
                    user.id +
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })