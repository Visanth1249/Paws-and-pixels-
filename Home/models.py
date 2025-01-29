from operator import truediv
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserRegistration(AbstractUser):
    """
    Custom user model for registration. Inherits from AbstractUser to utilize Django's
    built-in user authentication functionality.
    """
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=150, verbose_name="First Name")
    last_name = models.CharField(max_length=150, verbose_name="Last Name")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    address = models.TextField(blank=True, null=True, verbose_name="Address")

    def __str__(self):
        return self.username

class Accessory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='accessories/', null=True, blank=True, default='0')

    def __str__(self):
        return self.name

class Adoption(models.Model):
    animal_name = models.CharField(max_length=100, default='Unknown')
    breed = models.CharField(max_length=100, default='Unknown')
    description = models.TextField()
    available = models.BooleanField(default=True)  # Track if the pet is available
    animal_type = models.CharField(max_length=50)  # e.g., Dog, Cat, Bird
    image = models.ImageField(upload_to='adoptions/', null=True, blank=True, default='0')

    def __str__(self):
        return self.animal_name


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

# In Home/models.py
from django.db import models
from django.conf import settings  # Import settings

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)  # Make it nullable for now
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)  # Example related model
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.accessory.name}'

    def __str__(self):
        return f'{self.quantity} x {self.accessory.name}'


from django.conf import settings  # Import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.email}"
