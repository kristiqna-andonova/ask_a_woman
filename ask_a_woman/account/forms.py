from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from ask_a_woman.account.models import Profile


class CustomUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        # model = get_user_model()
        # fields = ('username', 'email', 'password1', 'password2')  # Ensure password fields are included
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        # }
        #
        # help_texts = {
        #     'username': 'Letters digits and @/./+/_ only.',
        #     'email': 'We’ll use this to send you account updates.',
        #     'password1': 'Your password must be at least 8 characters long.',
        #     'password2': 'Re-enter your password for confirmation.',
        # }


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = "__all__"


class UpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            User = get_user_model()
            # Ensure this email is unique except for the current user
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("This email is already in use. Please choose a different one.")
        return email



class ProfilePicForm(forms.ModelForm):
    profile_img = forms.ImageField(label="Profile Picture", required=False)

    profile_bio = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={ 'placeholder':'Profile Bio'}),
        required=False
    )

    facebook_link = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={ 'placeholder':'Facebook Link'}),
        required=False
    )

    instagram_link = forms.CharField(
        label="", widget=forms.TextInput(attrs={ 'placeholder':'Instagram Link'}),
        required=False
    )

    linkedin_link = forms.CharField(
        label="", widget=forms.TextInput(attrs={ 'placeholder':'LikedIn Link'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ("profile_img", "profile_bio", "facebook_link", "instagram_link", "linkedin_link")


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={ 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={ 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={ 'placeholder': 'Confirm New Password'})
    )

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        # Customize form field attributes if needed

