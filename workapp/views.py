from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import StudentRegistrationForm, DirectorRegistrationForm, SupervisorRegistrationForm, \
	StudentApplicationForm, PostingPlaceForm, WorkStatusForm, StudentApplicationForm2, UpdatePostingPlaceForm, \
	PostingPlaceForm2, SupervisorWorkStatusForm, BankDetailsForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User, PostingPlace, StudentApplication, BankDetails, WorkStatus
from datetime import date
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.forms import SetPasswordForm

# 2378123460, 202498765 (eliz1234), 20982389 (adex)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def student_registration(request):
	return redirect('register_student')


def login(request):
    return render(request, 'login.html')


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'


# Assuming a simple token storage mechanism (ideally should use Django's built-in tools)
tokens = {}

def request_password_reset(request):
    ctx ={}
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            print(f"user email => {user}")
            token = get_random_string(20)
            print(f"token => {token}")
            tokens[email] = token  # Store token (in production, use a more secure method)
            reset_url = request.build_absolute_uri(reverse('reset_password', args=[token]))
            print(f'reset url => {reset_url}')
            # Simulate sending email by displaying URL
            messages.success(request, f'Reset link: {reset_url}')
            ctx['reset_url'] = reset_url
        except User.DoesNotExist:
            ctx['error'] = 'User does not exist! Please, enter the correct email!'
        #ctx = {'error':error, 'reset_url':reset_url}
    return render(request, 'request_password_reset.html', ctx)



def reset_password(request, token):
    for email, stored_token in tokens.items():
        if stored_token == token:
            user = get_object_or_404(User, email=email)
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    del tokens[email]
                    messages.success(request, 'Your password has been successfully reset.')
                    return redirect('login')
            else:
                form = SetPasswordForm(user)
            return render(request, 'reset_password.html', {'form': form})
    messages.error(request, 'Invalid or expired token.')
    return redirect('request_password_reset')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.registration_date = date.today()            
            user.role = 'student'
            user.save()
            #login(request)
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register_student.html', {'form': form})


def register_director(request):
    if request.method == 'POST':
        form = DirectorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.registration_date = date.today()
            user.role = 'director'
            user.save()
            #login(request, user)
            return redirect('login')
    else:
        form = DirectorRegistrationForm()
    return render(request, 'register_director.html', {'form': form})



def register_supervisor(request):
    if request.method == 'POST':
        form = SupervisorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.registration_date = date.today()
            user.role = 'supervisor'
            user.save()
            
            return redirect('login')
    else:
        form = SupervisorRegistrationForm()
    return render(request, 'register_supervisor.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    # user = request.user
    if user.role == 'student':
        posting_places = PostingPlace.objects.all()
        applications = StudentApplication.objects.filter(student=request.user)
        app_count = applications.count()
        print(f"application for {user} => {app_count}")
        work_statuses = WorkStatus.objects.filter(
            application__student=user).order_by('day')
        work_statuses_count = work_statuses.count()
        #print(f'work status count => {work_statuses_count}')
        max_submissions = 6
        current_year = timezone.now().year
        user_dob = user.date_of_birth.year
        #print(f'cy => {current_year}')
        user_age = current_year - user_dob


        if request.method == 'POST':
            application_form = StudentApplicationForm(request.POST, request.FILES)
            posting_place_form = PostingPlaceForm2(request.POST)
            if 'apply_place' in request.POST:
                if application_form.is_valid():
                    print(f"student photo => {application_form}")
                    application = application_form.save(commit=False)
                    application.student = request.user
                    application.save()
                    return redirect('dashboard')
                else:
                    print('errors =>', application_form.errors)
            elif 'add_post_place' in request.POST:
                if posting_place_form.is_valid():
                    posting_place_form.save()
                    return redirect('dashboard')
        else:
            application_form = StudentApplicationForm()
            posting_place_form = PostingPlaceForm2()
    	
        
        try:
            bank_detail = BankDetails.objects.get(user=user)
            print(f" {user.username} bank details => {bank_detail}")
        except BankDetails.DoesNotExist:
            bank_detail = None

        ctx = {'posting_places': posting_places, 'applications': applications, 
                'application_form': application_form, 'posting_place_form':posting_place_form, 'app_count':app_count,
                 'work_statuses': work_statuses, 'user': user, 'work_statuses_count':work_statuses_count, \
                    'max_submissions':max_submissions, 'bank_detail':bank_detail, 'user':user, 'user_age':user_age}

        return render(request, 'student_dashboard.html', ctx)
    elif user.role == 'director':
        applications = StudentApplication.objects.all()
        supervisors = User.objects.filter(role='supervisor')
        posting_places = PostingPlace.objects.all()
        students = User.objects.filter(role='student')
        if request.method == 'POST':
            place_form = PostingPlaceForm(request.POST)
            if place_form.is_valid():
                place_form.save()
                return redirect('dashboard')
        else:
            place_form = PostingPlaceForm()
        ctx = {
            'applications': applications,
            'supervisors': supervisors,
            'students': students,
            'place_form': place_form,
            'posting_places':posting_places,
            'user': user
        }
        # return director dashboard
        return render(request, 'director_dashboard.html', ctx)
    elif user.role == 'supervisor':
        # Get the posting place assigned to the supervisor
        posting_place = PostingPlace.objects.filter(supervisor=user).first()
        #students_assigned = posting_place
        applications = StudentApplication.objects.filter(posting_place=posting_place).all()
        print(f"student applications => {applications}")
        students = []

        # Get the students assigned to the supervisor's posting place
        work_statuses = []
        if posting_place:
            students = User.objects.filter(applications__posting_place=posting_place).distinct()
            #print(f'students posted to your ppa => {students.applications}')
            work_statuses = WorkStatus.objects.filter(
                application__posting_place__supervisor=user).order_by('day')

	    	# Attach work statuses to each student
            for student in students:
                student.work_statuses = WorkStatus.objects.filter(application__student=student, 
	    			application__posting_place=posting_place)

        ctx = {
	        'user': user,
            #'students_assigned':students_assigned,
	        'posting_place': posting_place,
	        'students': students,
            'work_statuses': work_statuses,
            'applications':applications
	    }
        return render(request, 'supervisor_dashboard.html', ctx)
    else:
        # Handle other cases (optional)
        return render(request, 'other_dashboard.html')



@login_required
def application_detail(request, application_id):
    application = get_object_or_404(StudentApplication, id=application_id, student=request.user)
    director = User.objects.filter(role='director')
    supervisor_name = application.posting_place.supervisor.first_name if application.posting_place.supervisor else 'Supervisor not found!'
    #supervisor_name = application.posting_place.supervised_places.first().username if application.posting_place else 'No supervisor'
    return render(request, 'application_detail.html', {'application': application, 'supervisor_name': supervisor_name, 'director':director})



@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(StudentApplication, id=application_id)
    if request.method == 'POST':
        form = StudentApplicationForm2(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentApplicationForm2(instance=application)
    return render(request, 'update_application_status.html', {'form': form, 'application': application})


@login_required
def update_posting_place(request, posting_place_id):
    posting_place = get_object_or_404(PostingPlace, id=posting_place_id)
    if request.method == 'POST':
        form = UpdatePostingPlaceForm(request.POST, instance=posting_place)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to director dashboard after successful update
    else:
        form = UpdatePostingPlaceForm(instance=posting_place)
    return render(request, 'update_posting_place.html', {'form': form, 'posting_place': posting_place})


@login_required
def supervisor_detail(request, pk):
    supervisor = get_object_or_404(User, pk=pk, role='supervisor')
    supervised_places = PostingPlace.objects.filter(supervisor=supervisor)
    context = {
        'supervisor': supervisor,
        'supervised_places': supervised_places,
    }
    return render(request, 'supervisor_detail.html', context)


@login_required
def student_detail(request, pk):
    student = get_object_or_404(User, pk=pk, role='student')
    applications = StudentApplication.objects.filter(student=student)
    bank_details = BankDetails.objects.filter(user=student).first()
    work_statuses = WorkStatus.objects.filter(application__student=student)
    all_work_status_approved = all(ws.supervisor_checked for ws in work_statuses)
    # get latest student application
    latest_application = applications.latest('id') if applications.exists() else None

    try:
        bank_detail = BankDetails.objects.get(user=student)
        print(f" {student.username} bank details => {bank_detail}")
    except BankDetails.DoesNotExist:
        bank_detail = None

    context = {
        'student': student,
        'applications': applications,
        'bank_details': bank_details,
        'work_statuses': work_statuses,
        'all_work_status_approved': all_work_status_approved,
        'latest_application':latest_application,
        'bank_detail':bank_detail
    }
    return render(request, 'student_detail.html', context)


@login_required
def make_payment(request, student_id):
    student = get_object_or_404(User, pk=student_id, role='student')
    # Logic for making the payment (this can be a simple confirmation for now)
    # For example, setting a "paid" status on the student's applications or work statuses
    applications = StudentApplication.objects.filter(student=student, status='approved')
    applications.update(payment_status=True)
    # Redirect back to the student detail page
    return redirect('student_detail', pk=student.id)


@login_required
def approve_work_status(request, student_id, day):
    user = request.user
    if user.role != 'supervisor':
        print('Not a supervisor!')
        return redirect('dashboard')
    
    student = get_object_or_404(User, pk=student_id, role='student')
    posting_place = PostingPlace.objects.filter(supervisor=user).first()
    
    if not posting_place:
        messages.error(request, 'You do not have a posting place assigned.')
        return redirect('dashboard')
    
    application = StudentApplication.objects.filter(student=student, posting_place=posting_place, status='approved').first()
    
    if not application:
        messages.error(request, 'No approved application found for this student at your posting place.')
        return redirect('dashboard')
    
    work_status, created = WorkStatus.objects.get_or_create(application=application, day=day)
    
    if request.method == 'POST':
        work_status.supervisor_approval = True
        work_status.save()
        
        # Check if all weeks are approved by both student and supervisor
        all_weeks_checked = WorkStatus.objects.filter(application=application, student_checked=True, supervisor_approval=True).count()
        if all_weeks_checked == 6:
            application.work_completed = True
            application.save()
            messages.success(request, 'All weeks approved. Work completed.')
        elif all_weeks_checked > 6:
            messages.success(request, 'Total number of weeks reached!')
        else:
            messages.success(request, f'Work status for week {day} approved.')
        
        return redirect('dashboard')
    ctx =  {'work_status': work_status, 'week_number': week_number, 'student': student}

    return render(request, 'approve_work_status.html', ctx)


@login_required
def submit_work_status(request):
    if request.method == 'POST':
        form = WorkStatusForm(request.POST)
        if form.is_valid():
            work_status = form.save(commit=False)
            application = StudentApplication.objects.filter(student=request.user, status='approved').first()
            work_status.application = application
            work_status.student_checked = True
            work_status.save()
            messages.success(request, 'Work status submitted successfully.')
            return redirect('dashboard')
    else:
        form = WorkStatusForm()
    return render(request, 'submit_work_status.html', {'form': form})



@login_required
def add_bank_details(request):
    user = request.user
    if user.role != 'student':
        return redirect('dashboard')

    try:
        bank_details = BankDetails.objects.get(user=user)
    except BankDetails.DoesNotExist:
        bank_details = None

    if request.method == 'POST':
        bank_form = BankDetailsForm(request.POST, instance=bank_details)
        if bank_form.is_valid():
            bank_detail = bank_form.save(commit=False)
            bank_detail.user = user
            bank_detail.save()
            messages.success(request, 'Bank details updated successfully.')
            return redirect('dashboard')
    else:
        bank_form = BankDetailsForm(instance=bank_details)

    return render(request, 'add_bank_details.html', {'bank_form': bank_form, 'user': user})
