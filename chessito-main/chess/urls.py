from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    path('', include('main.urls')),

  
    path('onesignal_register/', user_views.onesignal_register, name='onesignal_register'),
               
    path('manifest.json', TemplateView.as_view(template_name='users/manifest.json', content_type='application/json')),
    path('OneSignalSDKWorker.js', TemplateView.as_view(template_name='users/OneSignalSDKWorker.js', content_type='application/x-javascript')),
    path('OneSignalSDKWorker.js', TemplateView.as_view(template_name='users/OneSignalSDKWorker.js', content_type='application/x-javascript')),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)