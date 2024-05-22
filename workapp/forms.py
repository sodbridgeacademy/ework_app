from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import User, StudentApplication, PostingPlace, BankDetails, WorkStatus


# all forms

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    matric_number = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES, required=False)
    registration_date = forms.DateField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'matric_number', 
        'department', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.registration_date = self.cleaned_data['registration_date']
        if commit:
            user.save()
        return user


class DirectorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'department', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    # class Meta:
    #     model = User
    #     fields = ['username', 'department', 'password1', 'password2']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Register'))


class SupervisorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    specialization = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', \
             'specialization', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class StudentApplicationForm2(forms.ModelForm):
    class Meta:
        model = StudentApplication
        #fields = ['posting_place']
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=StudentApplication.STATUS_CHOICES)
        }


class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = ['posting_place']
        # fields = ['status']
        # widgets = {
        #     'status': forms.Select(choices=StudentApplication.STATUS_CHOICES)
        # }


class PostingPlaceForm(forms.ModelForm):
    class Meta:
        model = PostingPlace
        fields = ['name', 'location', 'supervisor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the supervisor choices to only include users with the 'supervisor' role
        self.fields['supervisor'].queryset = User.objects.filter(role='supervisor')


class PostingPlaceForm2(forms.ModelForm):
    class Meta:
        model = PostingPlace
        fields = ['name', 'location']


class UpdatePostingPlaceForm(forms.ModelForm):
    class Meta:
        model = PostingPlace
        fields = ['name', 'location', 'supervisor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the supervisor choices to only include users with the 'supervisor' role
        self.fields['supervisor'].queryset = User.objects.filter(role='supervisor')



class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ['bank_name', 'account_number', 'account_name']



class WorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['week_number', 'student_checked']


class SupervisorWorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['supervisor_checked']