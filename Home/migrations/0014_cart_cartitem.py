# Generated by Django 3.1.12 on 2025-01-29 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0013_auto_20250129_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.accessory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.accessory')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.cart')),
            ],
        ),
    ]
