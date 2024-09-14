from rest_framework.serializers import ModelSerializer,CharField
from .models import PatientRecord,Patient
from users.serializer import UserHospitalSerializer

class RecordPatientSerializer(ModelSerializer):
    id = CharField(max_length=12)
    class Meta:
        model = Patient
        fields=['id','firstname','lastname','grandname','sex',"age",'date_of_birth',"phone","gmail"]
class PatientRecordSerializer(ModelSerializer):
    patient = RecordPatientSerializer()
    hospital =UserHospitalSerializer()
    class Meta:
        model=PatientRecord
        fields = ['id','patient',"reason",'hospital','date','Recommandation','type']
class PatientRelatedSerializer(ModelSerializer):
    patient = RecordPatientSerializer()
    hospital =UserHospitalSerializer()
    class Meta:
        model=PatientRecord
        fields = ['id','patient',"reason",'hospital','date','Recommandation','type']
class SearchPatientSerializer(ModelSerializer):
    id = CharField(max_length=12)
    class Meta:
        model = Patient
        fields=['id','firstname','lastname','grandname']
class DetailPatientSerializer(ModelSerializer):
    id = CharField(max_length=12)
    class Meta:
        model = Patient
        fields=['id','firstname','lastname','grandname','sex',"age",'date_of_birth',"pic",'phone','gmail']    
