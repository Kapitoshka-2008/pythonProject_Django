from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rename username field to Email for UX, Django still uses USERNAME_FIELD internally
        self.fields['username'].label = 'Электронная почта'
        self.fields['username'].widget = forms.EmailInput(attrs={'autocomplete': 'email'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country', 'first_name', 'last_name')


