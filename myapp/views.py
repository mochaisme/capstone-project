import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from myapp.EmailBackEnd import EmailBackEnd
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MahasiswaSignUpForm, DosenSignUpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def showLoginPage(request):
    return render(request, "login.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def mahasiswa_dashboard(request):
    return render(request, "mahasiswa_dashboard.html")

@login_required
def dosen_dashboard(request):
    pembimbing = get_object_or_404(Pembimbing, admin=request.user)
    bimbingan_list = Bimbingan.objects.filter(pembimbing=pembimbing)

    return render(request, 'dosen_dashboard.html', {'bimbingan_list': bimbingan_list})

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_dashboard")
            elif user.user_type == "2":
                return HttpResponseRedirect("/dosen_dashboard")
            elif user.user_type == "3":
                return HttpResponseRedirect("/mahasiswa_dashboard")
        else:
            return HttpResponse("Invalid login")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_mahasiswa(request):
    if request.method == 'POST':
        form = MahasiswaSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Mahasiswa berhasil didaftarkan!")
    else:
        form = MahasiswaSignUpForm()
    return render(request, 'register_mahasiswa.html', {'form': form})

def register_dosen(request):
    if request.method == 'POST':
        form = DosenSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Dosen berhasil didaftarkan!")
    else:
        form = DosenSignUpForm()
    return render(request, 'register_dosen.html', {'form': form})

# NEW SECTION HERE

from django.shortcuts import render, redirect
from .forms import PenelitianForm, BimbinganForm
from .models import Penelitian, Mhs

def tambah_penelitian(request):
    if request.method == 'POST':
        form = PenelitianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tambah_penelitian')  # Ganti sesuai URL tujuan setelah tambah
    else:
        form = PenelitianForm()
    return render(request, 'tambah_penelitian.html', {'form': form})

@login_required(login_url='/')
def tambah_bimbingan(request):
    try:
        mahasiswa = get_object_or_404(Mhs, admin=request.user)
        penelitian = Penelitian.objects.filter(nim=mahasiswa).first()

        if not penelitian:
            return HttpResponse("Anda belum memiliki penelitian yang terdaftar.")

        if request.method == 'POST':
            form = BimbinganForm(request.POST, request.FILES)
            if form.is_valid():
                bimbingan_obj = form.save(commit=False)
                bimbingan_obj.penelitian_id = penelitian
                bimbingan_obj.save()
                return HttpResponseRedirect('/mahasiswa_dashboard')  # atau redirect kemana pun
        else:
            form = BimbinganForm()

        return render(request, 'tambah_bimbingan.html', {'form': form})

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
from .models import Bimbingan, Pembimbing
from django.utils.timezone import now
from django.contrib import messages

@login_required
def approve_bimbingan(request, pk):
    bimbingan = get_object_or_404(Bimbingan, pk=pk)
    bimbingan.status = 'disetujui'
    bimbingan.save()
    messages.success(request, "Kegiatan disetujui.")
    return redirect('dosen_dashboard')

@login_required
def reject_bimbingan(request, pk):
    if request.method == 'POST':
        alasan = request.POST.get('alasan')
        bimbingan = get_object_or_404(Bimbingan, pk=pk)
        bimbingan.status = 'ditolak'
        bimbingan.komentar = alasan
        bimbingan.alasan_reject = alasan 
        bimbingan.save()
        messages.error(request, "Kegiatan ditolak.")
    return redirect('dosen_dashboard')








