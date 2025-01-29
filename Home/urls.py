from django.urls import path
from . import views
from .views import add_to_cart, view_cart, remove_from_cart
from .views import checkout, order_success
from django.conf import settings
from django.conf.urls.static import static
from .views import feedback_view

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('loginsuccess/', views.loginsuccess, name='loginsuccess'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('adoptions/', views.adoptions, name='adoptions'),
    path('accessories/', views.accessories, name='accessories'),
    path('feedback/', views.feedback, name='feedback'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('concern/', views.concern, name='concern'),
    path('restricted/', views.restricted_page, name='restricted_page'),
    path('logout/', views.logout_view, name='logout'),
    path('add_adoption/', views.add_adoption, name='add_adoption'),
    path('add_accessory/', views.add_accessory, name='add_accessory'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:accessory_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', views.increase_cart_quantity, name='increase_cart_quantity'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/count/', views.get_cart_count, name='get_cart_count'),
    path("checkout/", checkout, name="checkout"),
    path("order-success/", order_success, name="order_success"),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('submit-feedback/', feedback_view, name='submit-feedback'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from .views import checkout, order_success

