"""
URL configuration for proj1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from test1 import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin', admin.site.urls),
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('demo',views.demo,name='demo'),
    path('<int:pid>', views.details, name='details'),
    path('signup',views.signup1,name='signup1'),
    path('login',views.login1,name='login1'),
    path('logout/',views.logout1,name='logout1'),
    path('allproducts',views.allproducts,name='allproducts'),
    path('contactus',views.contactus,name='contactus'),
    path('contactus/add_record',views.add_record,name='add_record'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('search',views.search,name='search'),
    path('show',views.show,name='show'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('settings',views.settings,name="settings"),
    # path('profile1', views.profile1, name='profile1'),
    path('add_wishlists',views.add_wishlists,name='add_wishlists'),
    path('show_wishlists',views.show_wishlists, name='show_wishlists'),
    path('cart',views.cart,name='cart'),
    path('show_cart',views.show_cart,name='show_cart'),
    path('remove_item_cart',views.remove_item_cart,name='remove_item_cart'),
    path('remove_item_wishlist',views.remove_item_wishlist,name='remove_item_wishlist'),
    
    
    
    
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)