from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Wishlistt,Cart
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ContactForm



# Create your views here.

def home(request):
    myproduct = Product.objects.all().order_by('id')
    paginator = Paginator(myproduct, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'test1/home.html',{'page_obj':page_obj})


   #Filter  starts
   
def  allproducts(request):
    if request.method == 'GET':
        myproducts = Product.objects.all()
        return render(request,"test1/filter.html",{'x':myproducts})
    else:
        z = request.POST.get('myfood')
        # print (z)
        m = float(request.POST.get('price_range'))
        # print(m)
        if(z=='Select'):
            k = Product.objects.filter( price__lte=m )
        # k = Product.objects.filter(category=z)
        else:
            k = Product.objects.filter(category=z, price__lte=m )
        # print(k)
        # return HttpResponse('Hello')
        return render(request, "test1/filter.html", {'x': k,'j':m})
    
    #filter ends

def demo(request):
    myproduct = Product.objects.all()
    return render(request,'test1/demo.html',{'x':myproduct})

def signup1(request):
    if request.method == 'GET':
        return render(request,'test1/signup.html',{'form':UserCreationForm()})
    else:
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('login1')
            except IntegrityError:
                return render(request,'test1/signup.html',{'form':UserCreationForm(),'y':'Username already taken'})
            
        else:
            return render(request,'test1/signup.html',{'form':UserCreationForm(),'z':'Passwords Unmatched'})


       

def login1(request):
    if request.method == 'GET':
        return render(request,'test1/login.html',{'form':AuthenticationForm()})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'test1/login.html',{'form':AuthenticationForm(),'k':'Invalid Username or Password!'})


def logout1(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    if request.method == 'GET':
        logout(request)
        return redirect('home')

def contactus(request):
    form = ContactForm
    return render(request, 'test1/contactus.html',{'form': form})

def add_record(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        


# @login_required(login_url='login1')
def details(request,pid):
    if request.user.is_authenticated:
        myproduct = get_object_or_404(Product,pk=pid)
        return render(request,'test1/details.html',{'z':myproduct})
    else:
        if request.method == 'GET':
            return render(request,'test1/login.html',{'form':AuthenticationForm(),'o':'Login Required!'})
        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request,'test1/login.html',{'form':AuthenticationForm(),'k':'Invalid Username or Password!'})

def aboutus(request):
        return render(request,'test1/aboutus.html')



def search(request):
    # query = request.GET['query']
    if request.method == 'POST':
        query = request.POST.get('search1')
        # query = request.GET('search1')
        print(query)
        if len(query) > 0 :
            if Product.objects.filter(Title__icontains=query) | Product.objects.filter( category__icontains=query):
                if(Product.objects.filter(Title__icontains=query)):
                    k = Product.objects.filter(Title__icontains=query)
                    return render(request,"test1/search.html",{'x':k})
                if(Product.objects.filter(category__icontains=query)):
                    k = Product.objects.filter(category__icontains=query)
                    return render(request,"test1/search.html",{'x':k})
            else:
                return render(request,'test1/search.html',{'o':'Item Not Available'})
        else:
            return redirect("show")

def show(request):
    myproducts = Product.objects.all()
    return render(request,"test1/search.html",{'x':myproducts})

# def dashboard(request):
#     return render(request,"test1/dashboard.html")






def dashboard(request):
    return render(request,"test1/dashboard.html")

def settings(request):
    return render(request,"test1/settings.html")

def add_wishlists(request):
    if request.method=='POST':
        unmatch_objects = 0
        x = request.POST.get('w_btn')
        y = request.user.username
        k = Wishlistt.objects.all()
        items_no = Wishlistt.objects.all().count()
        # print(f'Number of items present in the model Wishlist2 {items_no}')
        # if no items in the model
        if items_no==0:
            wl_item = Wishlistt(username=y,wl_details=x)
            wl_item.save()
            print('user not present in the model')
            return redirect('home')
        else:
            # object in wishlist model
            for i in k:
                # if the user is exists in model
                if y == i.username:
                    z = Wishlistt.objects.filter(username=y, wl_details__contains=x).values()
                    # if the item is present in the wishlist
                    if z:
                        pass
                    # if the item is not present in the wishlist
                    else:
                        l = Wishlistt.objects.all()[unmatch_objects]
                        l.wl_details += ', ' + x
                        l.save()
                # if given user doesn't matched 
                else:
                    unmatch_objects += 1

            # NO object is found matched after checking whole model 
            if unmatch_objects == items_no:
                    wl_item = Wishlistt(username=y,wl_details=x)
                    wl_item.save()
        return redirect('home')
                    


def show_wishlists(request):
    username = request.user.username
    wishlist_details = Wishlistt.objects.filter(username=username).values().first()

    if wishlist_details and 'wl_details' in wishlist_details:
        wl_items = wishlist_details['wl_details'].split(', ')

        # Filter out empty strings and convert to integers
        wl_items = [int(item_id) for item_id in wl_items if item_id]

        # Ensure that c_items is not an empty list
        if wl_items:
            # Filter products based on the item IDs
            wl_products = Product.objects.filter(Product_id__in=wl_items)

            return render(request, "test1/dashboard.html", {'o': wl_products, 'wishlist':'YOUR WISHLIST'})
    
    # If cart is empty or no cart details found
    return render(request, 'test1/dashboard.html', {'l': 'Add items to Wishlist'})

                


def cart(request):
    if request.method=='POST':
        unmatch_objects = 0
        x = request.POST.get('c_btn')
        y = request.user.username
        print(x)
        print(y)
        k = Cart.objects.all()
        items_no = Cart.objects.all().count()
        # print(f'Number of items present in the model Wishlist2 {items_no}')
        # if no items in the model
        if items_no==0:
            c_item = Cart(username=y,c_details=x)
            c_item.save()
            print('user not present in the model')
            return redirect('home')
        else:
            # object in wishlist model
            for i in k:
                # if the user is exists in model
                if y == i.username:
                    z = Cart.objects.filter(username=y, c_details__contains=x).values()
                    # if the item is present in the wishlist
                    if z:
                        pass
                    # if the item is not present in the wishlist
                    else:
                        l = Cart.objects.all()[unmatch_objects]
                        l.c_details += ', ' + x
                        l.save()
                # if given user doesn't matched 
                else:
                    unmatch_objects += 1

            # NO object is found matched after checking whole model 
            if unmatch_objects == items_no:
                    c_item = Cart(username=y,c_details=x)
                    c_item.save()
        return redirect('home')
    
def show_cart(request):
    username = request.user.username
    cart_details = Cart.objects.filter(username=username).values().first()

    if cart_details and 'c_details' in cart_details:
        c_items = cart_details['c_details'].split(', ')

        # Filter out empty strings and convert to integers
        c_items = [int(item_id) for item_id in c_items if item_id]

        # Ensure that c_items is not an empty list
        if c_items:
            # Filter products based on the item IDs
            cart_products = Product.objects.filter(Product_id__in=c_items)

            return render(request, "test1/dashboard.html", {'p': cart_products, 'cart':'YOUR CART'})
    
    # If cart is empty or no cart details found
    return render(request, 'test1/dashboard.html', {'k': 'Add items to Cart'})
    



def remove_item_wishlist(request):
    if request.method=='POST':
        username = request.user.username
        item_id_to_remove = request.POST.get('rw_btn')
        # Retrieve the cart instance for the current user
        z = Wishlistt.objects.get(username=username)

        # Split the cart details string into a list of items
        wl_items = z.wl_details.split(', ')

        # Remove the specified item ID from the list
        wl_items.remove(str(item_id_to_remove))

        # Join the modified list back into a string
        updated_wishlists_details = ', '.join(wl_items)

        # Update the cart details and save the instance
        z.wl_details = updated_wishlists_details
        z.save()

        # Redirect to the cart page or display a success message
        return render(request, 'test1/dashboard.html')
    


def remove_item_cart(request):
    if request.method=='POST':
        username = request.user.username
        item_id_to_remove = request.POST.get('rc_btn')
        # Retrieve the cart instance for the current user
        z = Cart.objects.get(username=username)

        # Split the cart details string into a list of items
        c_items = z.c_details.split(', ')

        # Remove the specified item ID from the list
        c_items.remove(str(item_id_to_remove))

        # Join the modified list back into a string
        updated_cart_details = ', '.join(c_items)

        # Update the cart details and save the instance
        z.c_details = updated_cart_details
        z.save()

        # Redirect to the cart page or display a success message
        return render(request, 'test1/dashboard.html')

        
