from django.urls import path
from .views import (CustomAuthToken,getUser,getProfile,EditUser,GetDoctors,
                    getShowProfile,DeleteDoctors,ActiveDoctors,getVerify,Verify,createAccount)

urlpatterns = [
    path('get-auth-token',CustomAuthToken.as_view()),
    path('get-user',getUser.as_view()),
    path('get-profile',getProfile.as_view()),
    path('edit-user/<int:id>',EditUser.as_view()),
    path('get-doctors/',GetDoctors.as_view()),
    path('get-show-profile/',getShowProfile.as_view()),
    path("delete",DeleteDoctors.as_view()),
    path('active',ActiveDoctors.as_view()),
    path('get-verifys',getVerify.as_view()),
    path('verify',Verify.as_view()),
    path('create-account',createAccount.as_view())


]