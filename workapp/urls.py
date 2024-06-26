from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('logins/', views.custom_login, name='logins'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
	path('register/student/', views.register_student, name='register_student'),
	path('register/director/', views.register_director, name='register_director'),
    path('register/supervisor/', views.register_supervisor, name='register_supervisor'),
    path('reset/password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),

	path('dashboard/', views.dashboard, name='dashboard'),
    path('submit-report/', views.submit_work_status, name='submit_work_status'),
    path('update_application_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('supervisor/<int:pk>/', views.supervisor_detail, name='supervisor_detail'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('make_payment/<int:student_id>/', views.make_payment, name='make_payment'),
    #path('approve_work_status/<int:student_id>/', views.approve_work_status, name='approve_work_status'),
    path('approve_work_status/<int:student_id>/<str:day>/', views.approve_work_status, name='approve_work_status'),
    path('supervisor/work-status/<int:pk>/', views.supervisor_work_status_update, name='supervisor_work_status_update'),
    path('update_posting_place/<int:posting_place_id>/', views.update_posting_place, name='update_posting_place'),
    path('add_bank_details/', views.add_bank_details, name='add_bank_details'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
   
]
