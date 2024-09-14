from django.contrib import admin
from .models import Hospital,Patient,PatientRecord
# Register your models here.
class HospitalAdmin(admin.ModelAdmin):
    model=Hospital
    list_display=('name','level')
    search_fields = ['name',]
class PatientAdmin(admin.ModelAdmin):
    model=Patient
    list_display=('id',)
    search_fields = ['firstname',"lastname"]
class PatientRecordAdmin(admin.ModelAdmin):
    model=PatientRecord
    list_display=("patient",)

admin.site.register(Hospital,HospitalAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(PatientRecord,PatientRecordAdmin)
