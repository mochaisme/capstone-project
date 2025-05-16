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
    path('dosen_dashboard', views.dosen_dashboard),
    path('mahasiswa_dashboard', views.mahasiswa_dashboard, name='mahasiswa_dashboard'),
    path('register_mahasiswa/', views.register_mahasiswa, name='register_mahasiswa'),
    path('register_dosen/', views.register_dosen, name='register_dosen'), 
    path('tambah/', views.tambah_penelitian, name='tambah_penelitian'),
    path('tambah_bimbingan/', views.tambah_bimbingan, name='tambah_bimbingan'),
    path('milestone/logs/', views.deadline_log, name='deadline_log'),
    path('bimbingan/<int:pk>/', views.detail_bimbingan, name='detail_bimbingan'),
    path('bimbingan/<int:pk>/edit/', views.edit_bimbingan, name='edit_bimbingan'),
    path('bimbingan/<int:pk>/hapus/', views.hapus_bimbingan, name='hapus_bimbingan'),
    path('edit-deadline/', views.edit_deadline_dropdown, name='edit_deadline_dropdown'),
    path('milestone/<int:milestone_id>/upload/', views.upload_bukti_milestone, name='upload_bukti_milestone'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
