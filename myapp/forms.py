from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Mhs, Pembimbing

class MahasiswaSignUpForm(UserCreationForm):
    nama = forms.CharField(max_length=50)
    nim = forms.CharField(max_length=13)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'nama', 'nim')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 3  # Mahasiswa
        if commit:
            user.save()
            mhs = Mhs.objects.get(admin=user)
            mhs.nama_Mhs = self.cleaned_data['nama']
            mhs.nim = self.cleaned_data['nim']
            mhs.save()
        return user


class DosenSignUpForm(UserCreationForm):
    nama = forms.CharField(max_length=50)
    nip = forms.CharField(max_length=13)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'nama', 'nip')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2  # Dosen
        if commit:
            user.save()
            dosen = Pembimbing.objects.get(admin=user)
            dosen.nama_Dosen = self.cleaned_data['nama']
            dosen.nip = self.cleaned_data['nip']
            dosen.save()
        return user

# # NEW SECTION HERE
# from django import forms
# from .models import Bimbingan, Pembimbing

# class BimbinganForm(forms.ModelForm):
#     tanggal_mulai = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
#     tanggal_selesai = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

#     class Meta:
#         model = Bimbingan
#         fields = [
#             'tahun_semester', 'nama', 'deskripsi_kegiatan', 'tanggal_mulai', 'tanggal_selesai',
#             'tipe_penyelenggaraan', 'pembimbing', 'nama_dokumen', 'file', 'link'
#         ]
