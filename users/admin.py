from django.contrib import admin
from .models import MyUser,Doctor,Nurse,Verification
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm,CustomUserCreationForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ("username", "is_staff", "is_active",)
    list_filter = ("username", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ('Information',{'fields':('firstname','lastname',"sex")}),
        ('AddInformation',{'fields':('pic',)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",'firstname','lastname', "type",'pic','sex',"password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(MyUser, CustomUserAdmin)
class DoctorAdmin(admin.ModelAdmin):
    model = Doctor
    list_display =('hospital','user')
admin.site.register(Doctor,DoctorAdmin)
class NurseAdmin(admin.ModelAdmin):
    model = Nurse
    list_display =('hospital','user')
admin.site.register(Nurse,NurseAdmin)
class VerifyAdmin(admin.ModelAdmin):
    model =Verification
    list_display =('user','active')
admin.site.register(Verification,VerifyAdmin)