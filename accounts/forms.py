from django import forms
import re
from django.contrib.auth.forms import PasswordChangeForm,UserChangeForm
from . import models
from accounts.models import UserProfile


class UserRegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Email Id'})
    )

    first_name = forms.CharField(max_length=25, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))

    last_name = forms.CharField(max_length=25, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    password1 = forms.CharField(max_length=20, required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=20, required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Retype password'}))

    def check_space(self, username):
        for x in username:
            if x == ' ':
                return True

        return False

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if len(username) < 1:
            raise forms.ValidationError('Enter username!')
        else:
            check_username_space = self.check_space(username)

            if check_username_space:
                raise forms.ValidationError('Space are not allowed in username!')
            else:
                username_exist = models.CustomUser.objects.filter(username__iexact=username).exists()

                if username_exist:
                    raise forms.ValidationError('Already sign up with this username! Please change and try again!')
                else:
                    if len(email) < 1:
                        raise forms.ValidationError('Enter your email address!')
                    else:
                        email_correction = re.match(
                            '^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$',
                            email)
                        if not email_correction:
                            raise forms.ValidationError('Email format not correct!')
                        else:
                            email_exist = models.CustomUser.objects.filter(email__iexact=email).exists()

                            if email_exist:
                                raise forms.ValidationError(
                                    'Already sign up with this email! Please change and try again!')
                            else:
                                if len(password1) < 8:
                                    raise forms.ValidationError("Password is too short!")
                                else:
                                    if password1 != password2:
                                        raise forms.ValidationError("Password not matched!")
                                    else:
                                        if len(first_name) < 1:
                                            raise forms.ValidationError('Enter your first name!')
                                        else:
                                            if len(last_name) < 1:
                                                raise forms.ValidationError('Enter your last name!')

    def deploy(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        user = models.CustomUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password1)
        user.save()


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', max_length=20, required=False,
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))

    new_password1 = forms.CharField(label='New Password', max_length=20, required=False,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))

    new_password2 = forms.CharField(label='Confirm Password', max_length=20, required=False,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Retype Password'}))

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if len(new_password1) < 8:
            raise forms.ValidationError('Password must be minimum 8 digit!')
        else:
            if new_password1 != new_password2:
                raise forms.ValidationError('Password not matched!')
class EditProfileForm(UserChangeForm):

	class Meta:
		model = UserProfile
		fields =(
			'about_me',
            'current_city',
            'phone',
            'gender',
            'bio',
            'birth_date',
            'image',
			)

'''class EditProfileForm(UserChangeForm):
    class meta:
        model = UserProfile
        fields = (
            'about_me',
            'current_city',
            'phone',
            'gender',
            'bio',
            'birth_date',
            'image'
        )'''

'''
class ProfileForm(forms.Form):
    GenderChoice = (
        ('male', 'Male'),
        ('female', 'Female'),
    )


    about_me = forms.CharField(label='About me',max_length=200,required=False,
                                widget=forms.TextInput(attrs={'placeholder':
                                'Write about you within 200 letters! '}))
    current_city = forms.CharField(label='City',max_length=200, required=False,
                             widget = forms.TextInput(attrs={'placeholder': 'City!'}))
    phone = forms.CharField(label='Mobile',max_length=20, required=False,
                                widget=forms.TextInput(attrs={'placeholder': '01*********'}))
    gender = forms.ChoiceField( choices = GenderChoice)
    bio = forms.CharField(label='Bio Data',max_length=400, required=False,
                                widget=forms.Textarea(attrs={'placeholder': 'Bio data....'}))
    birth_date = forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget)
    image = forms.ImageField(label='Image', required=False,)

    def clean(self):
        about_me = self.cleaned_data.get('about_me')
        current_city = self.cleaned_data.get('current_city')
        phone = self.cleaned_data.get('phone')
        bio = self.cleaned_data.get('bio')
        birth_date = self.cleaned_data.get('birth_date')
        image = self.cleaned_data.get('image')

        if len(about_me) < 1 :
            raise forms.ValidationError('Write something about yourself ')
        else:
            if not image:
                raise forms.ValidationError('You must upload a image!')
            else:
                if len(phone) < 11 or len(phone) > 11 :
                    raise forms.ValidationError('Wirte your Phone number correctly')
                else:
                    if not current_city or not bio  :
                        raise forms.ValidationError('You must fill up the form correctly! ')

    def deploy(self):
        about_me = self.cleaned_data.get('about_me')
        current_city = self.cleaned_data.get('current_city')
        phone = self.cleaned_data.get('phone')
        bio = self.cleaned_data.get('bio')
        birth_date = self.cleaned_data.get('birth_date')
        image = self.cleaned_data.get('image')
        gender = self.cleaned_data.get('gender')

        user = models.UserProfile(
            about_me = about_me,
            current_city = current_city,
            phone =phone,
            bio = bio,
            birth_date =birth_date,
            image = image,
            gender = gender,
        )
        user.save()

'''

