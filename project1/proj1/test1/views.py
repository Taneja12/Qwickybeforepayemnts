from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login,logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # return HttpResponse('Hi')
    myproduct = Product.objects.all()
    paginator = Paginator(myproduct, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'test1/home.html',{'page_obj':page_obj})

def signupuser(request):
    if request.method == 'GET':
        return render(request,'test1/signupuser.html',{'form':UserCreationForm()})
    else:
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('home')
            except IntegrityError:
                return render(request,'test1/signupuser.html',{'form':UserCreationForm(),'y':'Username already taken'})



def loginuser(request):
    if request.method == 'GET':
        return render(request,'test1/loginuser.html',{'form':AuthenticationForm()})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'test1/loginuser.html',{'form':AuthenticationForm(),'k':'Combination is Incorrect'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')



def myhome(request):
    return render(request,'test1/myhome.html')

@login_required
def details(request,pid):
    myproduct = get_object_or_404(Product,pk=pid)
    return render (request,'test1/details.html',{'z':myproduct})

