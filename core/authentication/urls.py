from django.urls import path
from .views import *

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('update-bio/', BioUpdateView.as_view(), name='update-bio'),
    path('update-profile-pic/', ProfilePictureUpdateView.as_view(), name='update-profile-pic'),
    path('delete-profile-picture/', DeleteProfilePictureView.as_view(), name='delete-profile-picture'),
    path('logout/', LogoutView.as_view(), name='login'),
    path('user/<str:username>/', GetUserProfile.as_view(), name='user-profile'),
    path('me/', MyProfile.as_view(), name='my-profile'),
]