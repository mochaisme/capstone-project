from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from myapp.EmailBackEnd import EmailBackEnd
from .forms import MahasiswaSignUpForm, DosenSignUpForm, PenelitianForm, BimbinganForm, BuktiMilestoneForm
from .models import Bimbingan, Penelitian, Mhs, Milestone, DeadlineChangeLog
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

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
    try:
        mhs = get_object_or_404(Mhs, admin=request.user)
        penelitian = Penelitian.objects.filter(nim=mhs).first()
        if not penelitian:
            return HttpResponse("Belum ada data penelitian")

        bimbingans = Bimbingan.objects.filter(penelitian_id=penelitian)
        milestones = Milestone.objects.filter(penelitian_id=penelitian).order_by('deadline')

        # 💡 Update status berdasarkan deadline
        today = timezone.now().date()
        for m in milestones:
            if m.deadline:
                delta = (m.deadline - today).days
                if delta < 3:
                    m.status = "behind of schedule"
                elif delta < 30:
                    m.status = "on ideal schedule"
                else:
                    m.status = "Ahead of Schedule"
                m.save()

        stages = [
            "penetapan komisi pembimbing",
            "sidang komisi 1",
            "kolokium",
            "proposal",
            "penelitian dan bimbingan",
            "evaluasi dan monitoring",
            "sidang komisi 2",
            "seminar",
            "publikasi ilmiah",
            "ujian tesis"
        ]

        # Tentukan progress berdasarkan milestone terakhir
        milestone_terbaru = milestones.order_by('-updated_at').first()
        if milestone_terbaru and milestone_terbaru.jenis_milestone.lower() in stages:
            current_stage_index = stages.index(milestone_terbaru.jenis_milestone.lower()) + 1
        else:
            current_stage_index = 0

        progress = int((current_stage_index / len(stages)) * 100)
        logs = DeadlineChangeLog.objects.select_related('milestone', 'changed_by').order_by('-timestamp')
        # Gabungkan stages dan milestones
        milestone_info = []
        for i, stage in enumerate(stages):
            milestone_data = milestones[i] if i < len(milestones) else None
            milestone_info.append({
                'nama': stage,
                'deadline': milestone_data.deadline if milestone_data else None,
                'status': milestone_data.status if milestone_data else 'Belum tersedia',
                'id': milestone_data.id if milestone_data else None,
            })

        context = {
            'penelitian': penelitian,
            'bimbingans': bimbingans,
            'progress': progress,
            'current_stage': current_stage_index,
            'milestone_info': milestone_info,
            'logs': logs,
        }

        return render(request, "mahasiswa_dashboard.html", context)

    except Exception as e:
        return HttpResponse(f"Terjadi error: {str(e)}")

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


@login_required
def edit_deadline_dropdown(request):
    if request.method == 'POST':
        milestone_id = request.POST.get('milestone_id')
        new_deadline_str = request.POST.get('new_deadline')

        if not milestone_id or not new_deadline_str:
            return HttpResponse("Milestone dan deadline harus diisi.")

        # Gunakan variabel lain agar tidak bentrok dengan nama model
        ms = get_object_or_404(Milestone, id=milestone_id)

        try:
            new_deadline = datetime.strptime(new_deadline_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")

        if new_deadline != ms.deadline:
            DeadlineChangeLog.objects.create(
                milestone=ms,
                changed_by=request.user,
                old_deadline=ms.deadline,
                new_deadline=new_deadline,
            )
            ms.deadline = new_deadline
            ms.save()

        return redirect('mahasiswa_dashboard')
    
    return HttpResponse("Metode tidak valid")
    
# @login_required
# def edit_deadline(request, milestone_id):
#     ms = get_object_or_404(milestone, id=milestone_id)

#     if request.method == 'POST':
#         new_deadline_str = request.POST.get('new_deadline')
#         if not new_deadline_str:
#             return HttpResponse("Deadline tidak boleh kosong")

#         try:
#             new_deadline = datetime.strptime(new_deadline_str, '%Y-%m-%d').date()
#         except ValueError:
#             return HttpResponse("Format tanggal tidak valid. Gunakan YYYY-MM-DD")

#         if new_deadline != ms.deadline:
#             # Simpan log perubahan
#             DeadlineChangeLog.objects.create(
#                 milestone=ms,
#                 changed_by=request.user,
#                 old_deadline=ms.deadline,
#                 new_deadline=new_deadline,
#             )
#             ms.deadline = new_deadline
#             ms.save()

#         return redirect('mahasiswa_dashboard')

#     return render(request, 'edit_deadline.html', {'milestone': ms})


@login_required
def deadline_log(request):
    logs = DeadlineChangeLog.objects.select_related('milestone', 'changed_by').order_by('-timestamp')
    return render(request, 'deadline_log.html', {'logs': logs})

@login_required
def detail_bimbingan(request, pk):
    bimbingan = get_object_or_404(Bimbingan, pk=pk)
    return render(request, 'detail.html', {'bimbingan': bimbingan})

@login_required
def edit_bimbingan(request, pk):
    bimbingan = get_object_or_404(Bimbingan, pk=pk)
    
    if request.method == 'POST':
        form = BimbinganForm(request.POST, instance=bimbingan)
        if form.is_valid():
            form.save()
            return redirect('mahasiswa_dashboard')
    else:
        form = BimbinganForm(instance=bimbingan)

    return render(request, 'edit_bimbingan.html', {'form': form, 'bimbingan': bimbingan})

@login_required
def hapus_bimbingan(request, pk):
    bimbingan = get_object_or_404(Bimbingan, pk=pk)
    if request.method == 'POST':
        bimbingan.delete()
        return redirect('mahasiswa_dashboard')  # pastikan nama ini sesuai
    return render(request, 'bimbingan/confirm_delete.html', {'bimbingan': bimbingan})

def upload_bukti_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, id=milestone_id)  # Pastikan milestone selalu terdefinisi

    if request.method == 'POST':
        form = BuktiMilestoneForm(request.POST, request.FILES, instance=milestone)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.tanggal_upload = timezone.now()
            milestone.is_approved = 'pending'
            milestone.status = 'pending'
            milestone.save()
            return redirect('mahasiswa_dashboard')

    else:
        form = BuktiMilestoneForm(instance=milestone)

        return render(request, 'tambah_bimbingan.html', {'form': form})

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")






