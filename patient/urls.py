from django.urls import path
from .views import (getRecords,getPatients,getSearchPatient,createPatientRecord,createPatient,
                    PdfDetailRecord,getDetailRecord,getDetailpatient,PdfDetailPatient,
                    getPatientRelated,getHospital,EditRecord,RecordDelete,EditPatient,PatientDelete)

urlpatterns = [
    path('get-records',getRecords),
    path('get-patients',getPatients),
    path('get-search-patient',getSearchPatient),
    path('create-patient-record',createPatientRecord),
    path('create-patient',createPatient),
    path('pdf-detail-record/',PdfDetailRecord),
    path('get-record-detail/<int:id>',getDetailRecord),
    path('get-patient-detail/<str:id>',getDetailpatient),
    path('pdf-detail-patient/',PdfDetailPatient),
    path('get-patient-related/<str:id>',getPatientRelated),
    path('get-hospital',getHospital),
    path('edit-record/<str:id>',EditRecord),
    path('delete-record/<int:id>',RecordDelete),
    path('edit-patient/<str:id>',EditPatient),
    path('delete-patient/<str:id>',PatientDelete)
]