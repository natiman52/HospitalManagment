from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import PatientRecord,Patient,Hospital
from .seriliazer import (PatientRecordSerializer,RecordPatientSerializer,SearchPatientSerializer,DetailPatientSerializer,
                         PatientRelatedSerializer)
from django.db.models import Q
from users.serializer import UserHospitalSerializer,HospitalSerializer
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import json
from weasyprint import HTML,CSS
from django.conf import settings
import pathlib

# Create your views here.
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRecords(request):
    id =request.GET['id']
    name =request.GET['name']
    date =request.GET['date']
    if(id != "undefined"):
        if(date != 'undefined'):
            obj = PatientRecord.objects.filter(patient=id,date=date)
            serlizerObj = PatientRecordSerializer(obj,many=True)
        else:
            obj = PatientRecord.objects.filter(patient=id)
            serlizerObj = PatientRecordSerializer(obj,many=True)            
        print('fine here')
    elif(name != 'undefined'):
        if(date != 'undefined'):
            obj = PatientRecord.objects.filter(Q(patient__firstname__icontains=name) | Q(patient__lastname__icontains=name),date=date)
            serlizerObj = PatientRecordSerializer(obj ,many=True)
        else:
            obj = PatientRecord.objects.filter(Q(patient__firstname__icontains=name) | Q(patient__lastname__icontains=name))
            serlizerObj = PatientRecordSerializer(obj ,many=True)
    elif(date  != "undefined"):
        obj = PatientRecord.objects.filter(date=date)
        serlizerObj = PatientRecordSerializer(obj,many=True)
    else:
        obj =PatientRecord.objects.all()[:5]
        serlizerObj = PatientRecordSerializer(obj ,many=True)
    return Response(serlizerObj.data)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPatients(request):
    id =request.GET['id']
    name =request.GET['name']
    age =request.GET['age']
    if(id):
        obj = Patient.objects.filter(id=id)
        serlizerObj = RecordPatientSerializer(obj,many=True)
    elif(name):
        if(age):
            obj = Patient.objects.filter(Q(firstname__icontains=name) | Q(lastname__icontains=name),age=int(age))
            serlizerObj = RecordPatientSerializer(obj,many=True)
        else:
            obj = Patient.objects.filter(Q(firstname__icontains=name) | Q(lastname__icontains=name))
            serlizerObj = RecordPatientSerializer(obj,many=True)     
    else:
        if(age):
            obj = Patient.objects.filter(age=int(age))
            serlizerObj = RecordPatientSerializer(obj,many=True)  
        else:
            obj = Patient.objects.all()[:5]
            serlizerObj = RecordPatientSerializer(obj,many=True)            
    return Response(serlizerObj.data)



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSearchPatient(request):
    name =request.GET['name']
    obj = Patient.objects.filter(Q(firstname__icontains=name) | Q(lastname__icontains=name)| Q(grandname__icontains=name))
    serlizerObj = SearchPatientSerializer(obj,many=True)
    return Response(serlizerObj.data)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPatientRecord(request):
    id =request.data['id']
    reason =request.data['reason']
    recc =request.data['recc']
    hospital = request.data['hospital']
    cause = request.data['cause']
    if(hospital == ""):
        hospital = 1
    obj =PatientRecord(patient=Patient.objects.get(id=id),reason=reason,type=cause,Recommandation=recc,hospital=Hospital.objects.get(id=hospital))
    obj.save()
    return Response(status=201)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPatient(request):
    uid =request.data['uid']
    firstname =request.data['firstname']
    lastname =request.data['lastname']
    grandname =request.data['grandname']
    age =request.data['age']
    phone =request.data['phone']
    sex =request.data['sex']
    profile = request.data['profile']
    date_birth_date = request.data['date_birth_date']
    email =request.data['email']
    obj =Patient(id=uid,firstname=firstname,gmail=email,lastname=lastname,grandname=grandname,age=age,date_of_birth=date_birth_date,phone=phone,sex=sex,pic=profile)
    obj.save()
    return Response(status=201)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getDetailRecord(request,id):
    record =PatientRecord.objects.get(id=id)
    recordSer = PatientRecordSerializer(record)
    return Response(recordSer.data)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPatientRelated(request,id):
    patient =Patient.objects.get(id=id)
    record =PatientRecord.objects.filter(patient=patient)
    recordSer = PatientRelatedSerializer(record,many=True)
    return Response(recordSer.data)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getDetailpatient(request,id):
    record =Patient.objects.get(id=id)
    recordSer = DetailPatientSerializer(record)
    return Response(recordSer.data)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def PdfDetailRecord(request):
    request_Data =json.loads(request.GET['data']) 
    template_path = 'pdfTest.html'
    date =request_Data['date'].split('-')
    request_Data['date'] = f'{date[0]}/{date[1]}/{date[2]}'
    context = {'record': request_Data}

    print(date)
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment ;filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    css =CSS(string="@page {size:A4 landscape;margin:0}")
    pdf = HTML(string=html).write_pdf(stylesheets=[css])
    response.content = pdf
    # if error then show some funny view
    return response


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def PdfDetailPatient(request):
    request_Data =json.loads(request.GET['data'])
    date =request_Data['date_of_birth'].split('-')
    request_Data['date_of_birth'] = f'{date[0]}/{date[1]}/{date[2]}'
    img = request_Data['pic'].split('/media/')[1]
    test =pathlib.Path(settings.MEDIA_ROOT).as_uri()
    path = f"{os.path.join(test,img)}"
    request_Data['pic'] = path
    print(request_Data)
    template_path = 'pdfPatient.html'
    context = {'record': request_Data}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment ;filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    css =CSS(string="@page{size:A4;margin:10pt}")
    pisa_status = HTML(string=html).write_pdf(stylesheets=[css])
    # if error then show some funny view
    response.content = pisa_status
    return response


@api_view(["GET"])
def getHospital(request):
    keyword =request.GET['keyword']
    if(keyword != ""):
        record =Hospital.objects.filter(name__icontains=keyword)
        serlizerObj = UserHospitalSerializer(record,many=True)

    else:
        record =Hospital.objects.all()
        serlizerObj = HospitalSerializer(record,many=True)
    return Response(serlizerObj.data)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def EditRecord(request,id):
    recordObj = PatientRecord.objects.get(id=id)
    patient = request.data.get('patient')
    cause =request.data.get('cause')
    reason =request.data.get('reason')
    recc =request.data.get('recc')
    if(patient and cause and reason):
        newPatient = Patient.objects.get(id=patient)
        recordObj.reason =reason
        recordObj.type =cause
        if(recc):
            recordObj.Recommandation =recc
        recordObj.patient =newPatient
        recordObj.save()
        return Response(status=201)
    return Response(status=403)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def RecordDelete(request,id):
    obj =PatientRecord.objects.get(id=id)
    obj.delete()
    return Response(status=201)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def EditPatient(request,id):
    firstname =request.data['firstname']
    lastname =request.data['lastname']
    grandname =request.data['grandname']
    age =request.data['age']
    phone =request.data['phone']
    sex =request.data['sex']
    pic = request.data.get('pic')
    date = request.data['date']
    email =request.data['gmail']
    if(pic):
        obj = Patient(id=id,firstname=firstname,lastname=lastname,grandname=grandname,age=age,phone=phone,sex=sex,pic=pic,date_of_birth=date,gmail=email)
        if(not obj.DoesNotExist):
            obj.save()
    obj = Patient(id=id,firstname=firstname,lastname=lastname,grandname=grandname,age=age,phone=phone,sex=sex,date_of_birth=date,gmail=email)
    obj.save()
    return Response(status=201)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def PatientDelete(request,id):
    obj =Patient.objects.get(id=id)
    obj.delete()
    return Response(status=201)
