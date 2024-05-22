from django.contrib import admin
from .models import User, PostingPlace, StudentApplication

# Register your models here.
admin.site.register(User)
admin.site.register(PostingPlace)
admin.site.register(StudentApplication)
