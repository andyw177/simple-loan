from django.contrib import admin
from .models import *;
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(UserProfile)

admin.site.register(Lender)

admin.site.register(Property)

admin.site.register(Application)

admin.site.register(PreQualCriteria)


