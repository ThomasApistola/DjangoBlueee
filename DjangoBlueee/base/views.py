from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


def say_hello(request):
    return render(request, "base/hello.html")

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