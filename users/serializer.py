from rest_framework.serializers import ModelSerializer
from .models import MyUser,Doctor,Nurse,Verification
from patient.models import Hospital
class UserHospitalSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields=['id','name','location','level']
class HospitalSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields=['id','name','location','level','speciality','img']
class UserDoctorSerializer(ModelSerializer):
    hospital = UserHospitalSerializer()
    class Meta:
        model = Doctor
        fields = ['speciality','hospital']

class UserNurseSerializer(ModelSerializer):
    hospital = UserHospitalSerializer()
    class Meta:
        model = Nurse
        fields = ['Adreess','hospital']
        depth = 2    
class UserSerializer(ModelSerializer):
    profile = UserDoctorSerializer()
    class Meta:
        model=MyUser
        fields = ['username','firstname','lastname','sex','pic','type',"profile"]
        depth = 1

class UserSerializerNurse(ModelSerializer):
    profile2=UserNurseSerializer()
    class Meta:
        model=MyUser
        fields = ['username','firstname','lastname','sex','pic','type',"profile2"]
        depth = 1    
class AdminSerializer(ModelSerializer):
    class Meta:
        model=MyUser
        fields = ['username','firstname','lastname','sex','pic','type']
        depth = 1 
## Profile after this
class ProfileHospitalSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields=['name',"location",'level','speciality']
class ProfileDoctorSerializer(ModelSerializer):
    hospital = ProfileHospitalSerializer()
    class Meta:
        model = Doctor
        fields = ['speciality','hospital','Adreess']
        depth = 2

class ProfileNurseSerializer(ModelSerializer):
    hospital = ProfileHospitalSerializer()
    class Meta:
        model = Nurse
        fields = ['Adreess','hospital']
        depth = 2    
class ProfileSerializer(ModelSerializer):
    profile = ProfileDoctorSerializer()
    class Meta:
        model=MyUser
        fields = ['id','username','firstname','lastname',"grandname",'sex','pic','type',"profile","is_active"]
        depth = 4
class ProfileAdminSerializer(ModelSerializer):
    class Meta:
        model=MyUser
        fields = ['id','username','grandname','firstname','lastname','sex','pic','type']
        depth = 1 
class ProfileSerializerNurse(ModelSerializer):
    profile2 = ProfileNurseSerializer()
    class Meta:
        model=MyUser
        fields = ['id','username','firstname','lastname','sex','pic','type',"profile2"]
        depth = 2  


## Doctor GET Serializers

class DoctorUserSerializer(ModelSerializer):
    class Meta:
        model=MyUser
        fields = ['username','firstname','lastname','grandname','pic']
        depth = 2  
class DoctorSerializer(ModelSerializer):
    user =DoctorUserSerializer()
    class Meta:
        model = Doctor
        fields = ['id','user','speciality','Adreess']
        depth = 1

## Verification Serializer
class verifyUserSerializer(ModelSerializer):
    class Meta:
        model =MyUser
        fields =['id','firstname','lastname','grandname','is_active','username']     
class VerifySerializer(ModelSerializer):
    class Meta:
        model =Verification
        fields = ['id','user','type','active']
        depth =2