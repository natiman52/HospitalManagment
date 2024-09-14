from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken,APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import (UserSerializer,UserSerializerNurse,ProfileSerializer,ProfileSerializerNurse,AdminSerializer,
                         DoctorSerializer,ProfileAdminSerializer,VerifySerializer)
from .models import MyUser,Doctor,Verification,Nurse
from .forms import CustomUserCreationForm,CustomUserCreationFormSelf
from patient.models import Hospital
## non_field_errors
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'type': user.type,
        })
    
class getUser(APIView):
    def post(self,request,*args,**Kwargs):
        userObj = Token.objects.get(key=request.data['key']).user
        if (userObj.type == 'Doctor'):
            userSer = UserSerializer(userObj)
        elif(userObj.type == "Nurse"):
            userSer = UserSerializerNurse(userObj)
        else:
            userSer =AdminSerializer(userObj)
        return Response(userSer.data)

class getProfile(APIView):
    def post(self,request,*args,**Kwargs):
        userObj = Token.objects.get(key=request.data['key']).user
        print(request.data)
        if (userObj.type == 'Doctor'):
            userSer = ProfileSerializer(userObj)
            print('testing')
        elif(userObj.type == "Nurse"):
            userSer = ProfileSerializerNurse(userObj)
        else:
            userSer=ProfileAdminSerializer(userObj)
        return Response(userSer.data)

class getShowProfile(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request,*args,**Kwargs):
        userObj = Doctor.objects.get(id=request.data['id'])
        ser =ProfileSerializer(userObj.user)
        return Response(ser.data)
   
class EditUser(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request,id,*args,**kwargs):
        obj =MyUser.objects.get(id=id)
        pic =request.data['pic']
        firstname =request.data['firstname']
        lastname =request.data['lastname']
        grandname =request.data['grandname']
        username =request.data['username']
        sex =request.data['sex']
        special =request.data.get('special')
        adrress =request.data.get('adrress')
        obj.pic = pic
        obj.firstname =firstname
        obj.lastname =lastname
        obj.grandname =grandname
        obj.username =username
        obj.sex =sex
        obj.save()
        if(obj.type == 'Doctor'):
            objProfile =Doctor.objects.get(user=obj)
            objProfile.speciality =special
            objProfile.Adreess =adrress
            objProfile.save()
            return Response({'true':'true'})
        elif(obj.type == "Nurse"):
            objProfile =Nurse.objects.get(user=obj)
            objProfile.Adreess =adrress
            objProfile.save()
            return Response({'true':'true'})
        return Response({'true':'true'})

        
class GetDoctors(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request,*args,**kwargs):
        obj =Doctor.objects.all()
        objSer =DoctorSerializer(obj,many=True)
        return Response(objSer.data)
class DeleteDoctors(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request,*args,**kwargs):
        print(request.data)
        id =request.data['id']
        doctor =Doctor.objects.get(id=id)
        doctor.user.delete()
        return Response(status=201)
class ActiveDoctors(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request,*args,**kwargs):
        print(request.data)
        id =request.data['id']
        doctor =Doctor.objects.get(id=id)
        doctor.user.is_active = not doctor.user.is_active
        doctor.user.save()
        return Response(status=201)

class getVerify(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request,*args,**kwargs):
        obj =Verification.objects.filter(active=True)
        serObj =VerifySerializer(obj,many=True)
        return Response(serObj.data)  
class Verify(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request,*args,**kwargs):
        obj =Verification.objects.get(id=request.data['id'])
        if(request.data['act'] == 'cancel'):
            obj.active =False
            obj.save()
            return Response(status=201)  
        obj.user.is_active = True
        obj.user.save()
        obj.active = False
        obj.save()
        return Response(status=201)  
    
class createAccount(APIView):
    def post(self,request,*args,**kwargs):
        obj =CustomUserCreationFormSelf(request.data)
        print(request.data)
        hospital =request.data['hospital']
        type = request.data['type']
        adreess = request.data['adreess']
        special =request.data.get('special')
        phone =request.data['phone']
        email =request.data['email']
        if(obj.is_valid()):
            if(type == 'Nurse'):
                NurseObj =Nurse(user=obj.instance,hospital=Hospital.objects.get(id=int(hospital)),Adreess=adreess)
                obj.save()
                NurseObj.save()
                return Response(status=201)
            else:
                DoctorObj =Doctor(user=obj.instance,hospital=Hospital.objects.get(id=int(hospital)),Adreess=adreess,speciality=special)
                obj.save()
                DoctorObj.save()
                return Response(status=201) 
        return Response({"message":obj.errors.as_data()},status=405)