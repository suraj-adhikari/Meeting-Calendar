
from django.contrib import admin
from django.urls import path,include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('hubspot_auth',views.hubspot_auth,name='hubspot_auth'),
    path('hubspot/callback',views.hubspot_callback,name='signup'),
    path('logout/',views.LogoutPage,name='logout'),
    # path('/api', include('api.urls')),
    # path('home/',views.HomePage,name='home'),
    # path('user/',views.user,name='user'),
]
