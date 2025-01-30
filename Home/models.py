from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# -------------------- User Model --------------------
class UserRegistration(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=150, verbose_name="First Name")
    last_name = models.CharField(max_length=150, verbose_name="Last Name")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    address = models.TextField(blank=True, null=True, verbose_name="Address")

    def __str__(self):
        return self.username


# -------------------- Accessory Model --------------------
class Accessory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accessories/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)  # Track available stock

    def __str__(self):
        return self.name


# -------------------- Adoption Model --------------------
class Adoption(models.Model):
    animal_name = models.CharField(max_length=100, default='Unknown')
    breed = models.CharField(max_length=100, default='Unknown')
    description = models.TextField()
    available = models.BooleanField(default=True)  # Track if the pet is available
    animal_type = models.CharField(max_length=50)  # e.g., Dog, Cat, Bird
    image = models.ImageField(upload_to='adoptions/', null=True, blank=True, default='0')

    def __str__(self):
        return self.animal_name


# -------------------- Cart & Cart Items --------------------
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.accessory.name}'


# -------------------- Order & Order Items --------------------
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.email}"

    def finalize_order(self, cart_items):
        """
        Deducts stock when an order is placed and clears the cart.
        """
        for item in cart_items:
            if item.accessory.quantity < item.quantity:
                raise ValueError(f"Not enough stock for {item.accessory.name}")

            # Deduct stock
            item.accessory.quantity -= item.quantity
            item.accessory.save()

            # Create OrderItem entry
            OrderItem.objects.create(order=self, accessory=item.accessory, quantity=item.quantity)

        # Clear the cart
        cart_items.delete()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.accessory.name} (Order {self.order.id})"
