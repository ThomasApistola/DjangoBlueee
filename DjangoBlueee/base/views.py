from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NameForm, ProfileForm, MedicineForm, CollectionForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Profile, Medicine, Collection
from django.contrib.auth.models import User
# Create your views here.

def index (request):
        return render(request, "base/index.html")

def nameform(requests):
    form = NameForm()
    context = {"form": form}
   
    if requests.method == "POST":
        name = requests.POST.get("your_name")
        context["greeting"] = f"Welcome {name}!"
    return render(requests, "base/nameform.html", context)

def register(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect("index")
  else:
      form = UserCreationForm()
 
       
  context = {"form": form}
  return render(request, "registration/register.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    context = {"user": request.user, "profile": profile}
    return render(request, "base/profile.html", context)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
 
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        # Set the form to the existing profile instance, so the form is pre-filled
        form = ProfileForm(instance=profile)
 
    return render(request, "base/edit_profile.html", {"form": form})

@staff_member_required
def create_collection(request):
    initial = {}
    medicine_id = request.GET.get('medicine')
    if medicine_id:
        try:
            initial['medicine'] = Medicine.objects.get(pk=medicine_id)
        except Medicine.DoesNotExist:
            pass
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            user = request.POST.get('user')
            medicine = request.POST.get('medicine')
            date = request.POST.get('date')
            # Check of er al een afhaalactie bestaat voor deze gebruiker, medicijn en datum
            bestaat = Collection.objects.filter(user=user, medicine=medicine, date=date).exists()
            if bestaat:
                form.add_error(None, "Deze gebruiker heeft op deze dag al een afhaalactie voor dit medicijn.")
            else:
                form.save()
                messages.success(request, "Afhaalactie aangemaakt.")
                return redirect('admin_collection_list')
    else:
        form = CollectionForm(initial=initial)
    return render(request, "base/create_collection.html", {"form": form})

@staff_member_required
def admin_collection_list(request):
    collections = Collection.objects.all()
    return render(request, "base/admin_collection_list.html", {"collections": collections})

@staff_member_required
def delete_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if request.method == "POST":
        collection.delete()
        messages.success(request, "Afhaalactie verwijderd.")
        return redirect('admin_collection_list')
    return render(request, "base/delete_collection.html", {"collection": collection})

@staff_member_required
def approve_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    if request.method == "POST":
        collection.collected_approved = True
        collection.collected_approved_by = request.user
        collection.save()
        messages.success(request, "Afhaalactie goedgekeurd.")
        return redirect('admin_collection_list')
    return render(request, "base/approve_collection.html", {"collection": collection})

@staff_member_required
def create_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicijn aangemaakt.")
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, "base/create_medicine.html", {"form": form})

@staff_member_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, "base/medicine_list.html", {"medicines": medicines})

@staff_member_required
def edit_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicijn aangepast.")
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, "base/edit_medicine.html", {"form": form, "medicine": medicine})

@staff_member_required
def delete_medicine(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == "POST":
        medicine.delete()
        messages.success(request, "Medicijn verwijderd.")
        return redirect('medicine_list')
    return render(request, "base/delete_medicine.html", {"medicine": medicine})

@login_required
def user_collections(request):
    openstaande = Collection.objects.filter(user=request.user, collected=False)
    not_yet_collected = Collection.objects.filter(user=request.user, collected=True, collected_approved=False)
    return render(request, "base/user_collections.html", {
        "openstaande": openstaande,
        "not_yet_collected": not_yet_collected,
    })

@login_required
def mark_collected(request, pk):
    collection = Collection.objects.get(pk=pk, user=request.user)
    if request.method == "POST":
        collection.collected = True
        collection.save()
        messages.success(request, "Afhaalactie gemarkeerd als opgehaald. Wacht op goedkeuring door admin.")
        return redirect('user_collections')
    return render(request, "base/mark_collected.html", {"collection": collection})

@staff_member_required
def user_profile_admin(request, user_id):
    user = User.objects.get(pk=user_id)
    collections = user.collection_set.all().select_related('medicine')
    return render(request, "base/user_profile_admin.html", {
        "profile_user": user,
        "collections": collections,
    })

@login_required
def medicine_detail(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    # Hoe vaak heeft de huidige gebruiker dit medicijn opgehaald
    user_count = Collection.objects.filter(
        medicine=medicine, user=request.user, collected=True, collected_approved=True
    ).count()
    # Hoe vaak is het medicijn in totaal opgehaald (alle gebruikers)
    total_count = Collection.objects.filter(
        medicine=medicine, collected=True, collected_approved=True
    ).count()
    return render(request, "base/medicine_detail.html", {
        "medicine": medicine,
        "user_count": user_count,
        "total_count": total_count,
    })

@login_required
def custom_password_change(request):
    error = ""
    success = False
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        user = request.user

        if not user.check_password(old_password):
            error = "Oud wachtwoord is onjuist."
        elif new_password1 != new_password2:
            error = "Wachtwoorden komen niet overeen."
        elif not new_password1:
            error = "Nieuw wachtwoord mag niet leeg zijn."
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            success = True
    return render(request, "registration/password_change.html", {"error": error, "success": success})