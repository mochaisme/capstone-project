import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from myapp.EmailBackEnd import EmailBackEnd
from django.shortcuts import render, redirect
from .forms import MahasiswaSignUpForm, DosenSignUpForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def showLoginPage(request):
    return render(request, "login.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

def dosen_dashboard(request):
    return render(request, "dosen_dashboard.html")

def mahasiswa_dashboard(request):
    return render(request, "mahasiswa_dashboard.html")

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

# # NEW SECTION HERE
# from .forms import BimbinganForm
# from .models import Pembimbing
# from django.http import JsonResponse

# def mahasiswa_dashboard(request):
#     return render(request, "mahasiswa_dashboard.html")

# def tambah_bimbingan(request):
#     if request.method == 'POST':
#         form = BimbinganForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/mahasiswa_dashboard')
#     else:
#         form = BimbinganForm()
#     return render(request, 'tambah_bimbingan.html', {'form': form})





