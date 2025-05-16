from django.urls import path
from myapp import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    path('home', views.home),
    path('admin/', admin.site.urls),
    path('', views.showLoginPage),
    path('get_user_detail', views.GetUserDetails),
    path('logout_user', views.logout_user),
    path('doLogin', views.doLogin),
    path('admin_dashboard', views.admin_dashboard),
    path('mahasiswa_dashboard', views.mahasiswa_dashboard),
    path('register_mahasiswa/', views.register_mahasiswa, name='register_mahasiswa'),
    path('register_dosen/', views.register_dosen, name='register_dosen'), 
    path('tambah/', views.tambah_penelitian, name='tambah_penelitian'),
    path('tambah_bimbingan/', views.tambah_bimbingan, name='tambah_bimbingan'),
    # NEW SECTION HERE
    path('dosen_dashboard', views.dosen_dashboard, name='dosen_dashboard'),
    path('bimbingan/<int:pk>/approve/', views.approve_bimbingan, name='approve_bimbingan'),
    path('bimbingan/<int:pk>/reject/', views.reject_bimbingan, name='reject_bimbingan'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)