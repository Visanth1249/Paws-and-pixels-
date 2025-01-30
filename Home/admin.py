from django.contrib import admin
from .models import UserRegistration
# Register your models here.
admin.site.register(UserRegistration)
from django.contrib import admin
from .models import Accessory, Adoption

admin.site.register(Accessory)
admin.site.register(Adoption)

from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # Only reduce quantity on new orders
            if obj.accessory.quantity >= obj.quantity:
                obj.accessory.quantity -= obj.quantity
                obj.accessory.save()
            else:
                raise ValueError("Not enough stock available.")
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderAdmin)
