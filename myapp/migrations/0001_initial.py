# Generated by Django 4.2.8 on 2023-12-21 19:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField(unique=True)),
                ('type', models.CharField(choices=[('Twin', 'Twin'), ('King', 'King'), ('Suite', 'Suite')], max_length=20)),
                ('price', models.IntegerField()),
                ('max_guests', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='room_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_no', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('checkin_date', models.DateField()),
                ('checkout_date', models.DateField()),
                ('TEST_cc_no', models.CharField(max_length=20)),
                ('TEST_cc_exp', models.CharField(max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.guest')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.room')),
            ],
        ),
    ]