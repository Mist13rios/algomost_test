from django.contrib import admin
from .models import ShowcaseItem, Specializations, UserPoll, AppUser
# Register your models here.

admin.site.register(ShowcaseItem)
admin.site.register(Specializations)
admin.site.register(UserPoll)
admin.site.register(AppUser)
