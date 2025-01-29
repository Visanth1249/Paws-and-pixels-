from django.contrib import admin
from .models import UserRegistration
# Register your models here.
admin.site.register(UserRegistration)
from django.contrib import admin
from .models import Accessory, Adoption

admin.site.register(Accessory)
admin.site.register(Adoption)

