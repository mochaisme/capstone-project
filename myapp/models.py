from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1, "admin"), (2, "pembimbing"), (3, "mahasiswa"))
    user_type=models.CharField(default=1, choices=user_type_data, max_length=10)

class Mhs(models.Model):
    id=models.AutoField(primary_key=True)
    nim=models.CharField(max_length=13)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

class Pembimbing(models.Model):
    id=models.AutoField(primary_key=True)
    nip=models.CharField(max_length=15)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

class AdminIPB(models.Model):
    id=models.AutoField(primary_key=True)
    nip=models.CharField(max_length=50)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

class Penelitian(models.Model):
    penelitian_id=models.AutoField(primary_key=True)
    nama_Mhs=models.CharField(max_length=50, null=True)
    nama_Dosen=models.CharField(max_length=50, null=True)
    nim=models.ForeignKey(Mhs, on_delete=models.CASCADE)
    nip=models.ForeignKey(Pembimbing, on_delete=models.CASCADE)
    judul=models.CharField(max_length=150)
    STATUS_CHOICES = [
        ('penetapan komisi pembimbing', 'Penetapan Komisi Pembimbing'),
        ('sidang komisi 1', 'Sidang Komisi 1'),
        ('kolokium', 'Kolokium'),
        ('proposal', 'Proposal'),
        ('penelitian dan bimbingan', 'Penelitian dan Bimbingan'),
        ('evaluasi dan monitoring', 'Evaluasi dan Monitoring'),
        ('sidang komisi 2', 'Sidang Komisi 2'),
        ('seminar', 'Seminar'),
        ('publikasi ilmiah', 'Publikasi Ilmiah'),
        ('ujian tesis', 'Ujian Tesis')
    ]
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, default='Penetapan Komisi Pembimbing')
    tanggal_mulai=models.DateTimeField(auto_now=False, auto_now_add=False)
    
class milestone(models.Model):
    id=models.AutoField(primary_key=True)
    penelitian_id=models.ForeignKey(Penelitian, on_delete=models.CASCADE)
    jenis_milestone=models.CharField(max_length=30)
    deadline=models.DateField(max_length=20)
    STATUS_CHOICES = [
        ('ahead of schedule', 'Ahead of Schedule'),
        ('on ideal schedule', 'On Ideal Schedule'),
        ('behind the schedule', 'Behind The Schedule')
    ]
    status=models.CharField(max_length=30, choices=STATUS_CHOICES, default='ahead of schedule')

class bimbingan(models.Model):
    id=models.AutoField(primary_key=True)
    penelitian_id=models.ForeignKey(Penelitian, on_delete=models.CASCADE)
    tahun_semester=models.CharField(max_length=20)
    nama=models.CharField(max_length=70)
    deskripsi_kegiatan=models.CharField(max_length=200)
    TIPE_PENYELENGGARAAN_CHOICES = [
        ('hybrid', 'Hybrid'),
        ('offline', 'Offline'),
        ('online', 'Online'),
    ]
    tipe_penyelenggaraan = models.CharField(
        max_length=10,
        choices=TIPE_PENYELENGGARAAN_CHOICES,
        default='offline',
    )
    tanggal=models.DateTimeField()
    komentar=models.CharField(max_length=500)
    STATUS_CHOICES = [
        ('sedang diperiksa', 'Sedang Diperiksa'),
        ('disetujui', 'Disetujui'),
        ('ditolak', 'Ditolak')
    ]
    pembimbing=models.ForeignKey(Pembimbing, on_delete=models.CASCADE)
    nama_dokumen = models.CharField(
        max_length=255,
        help_text="Sertifikat Kegiatan, LOA, Laporan Kegiatan, Photo/Dokumentasi Kegiatan, dll"
    )
    file = models.FileField(
        upload_to='dokumen_pendukung/',
        help_text="Maksimum upload: 10MB. Jika lebih, upload ke tempat lain dan masukkan alamatnya pada bagian Link."
    )
    link = models.URLField(
        help_text="URL yang merujuk kepada informasi kegiatan (website, media sosial, drive, dll)"
    )
    def __str__(self):
        return self.nama

class Notifikasi(models.Model):
    id=models.AutoField(primary_key=True)
    nim=models.ForeignKey(Mhs, on_delete=models.CASCADE)
    isi=models.CharField(max_length=200)
    waktu_kirim=models.DateTimeField(auto_now=False, auto_now_add=False)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminIPB.objects.create(admin=instance)
        if instance.user_type==2:
            Pembimbing.objects.create(admin=instance)
        if instance.user_type==3:
            Mhs.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminipb.save()
    if instance.user_type==2:
        instance.pembimbing.save()
    if instance.user_type==3:
        instance.mhs.save()