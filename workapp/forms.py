from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
        fields = ['first_name', 'last_name', 'matric_number', 'email', 'phone_number', 'date_of_birth', 'gender', 
        'department', 'faculty', 'password1', 'password2']


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
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES, required=True)
    #department = forms.CharField(max_length=100)
    #date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'staff_id', 'email', 'gender', 'password1', 'password2']

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
    #specialization = forms.CharField(max_length=100)
    #date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'staff_id', 'email', 'gender', \
             'department', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None



class AACustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username/Matric No/Staff ID",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username/Matric No/Staff ID'})
    )
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
        ('director', 'Director')
    ]
    role = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='User Type', required=True)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username (Staff ID or Matric Number)", max_length=50)
    role = forms.ChoiceField(label="User Type", choices=[('student', 'Student'), ('supervisor', 'Supervisor'), ('director', 'Director')])



class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        #fields = ['posting_place']
        # fields = ['status']
        # widgets = {
        #     'status': forms.Select(choices=StudentApplication.STATUS_CHOICES)
        # }

        fields = [
            'posting_place', 'student_photo', 'room_number', 'cgpa',  'year_of_study',
            'reason_for_desiring_to_work', 'hod_recommendation_letter'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'date_signed': forms.DateInput(attrs={'type': 'date'}),
        }


class StudentApplicationForm2(forms.ModelForm):
    class Meta:
        model = StudentApplication
        #fields = ['posting_place']
        fields = ['status', 'signature', 'date_signed']
        widgets = {
            'status': forms.Select(choices=StudentApplication.STATUS_CHOICES),
            'date_signed': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'form-control'
            }),
        }



class StudentApplicationForm3(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = ['supervisor_approval']



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




class StudentCommentUpdate(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['comments']


class SupervisorCommentUpdate(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['supervisor_comment']



class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = BankDetails
        fields = ['bank_name', 'account_number', 'account_name']



class WorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['date', 'day', 'start_time', 'end_time', 'comments']

        widgets = {
            'date': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'form-control'
            }),
            'start_time':forms.TextInput(attrs=
                {'placeholder':'E.g. 8am',
                'class': 'form-control'
                }),
            'end_time':forms.TextInput(attrs=
                {'placeholder':'E.g. 3pm'
                }),
        }


class SupervisorWorkStatusForm(forms.ModelForm):
    class Meta:
        model = WorkStatus
        fields = ['supervisor_comment']