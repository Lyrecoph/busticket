# Generated by Django 4.1.13 on 2024-07-06 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=150)),
                ('destination', models.CharField(max_length=150)),
                ('departure_datetime', models.DateTimeField()),
                ('available_seats', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Trajet',
                'verbose_name_plural': 'Trajets',
                'unique_together': {('origin', 'destination', 'departure_datetime')},
            },
        ),
        migrations.CreateModel(
            name='BooKing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_seats', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('confirmed', 'Confirmed'), ('pending', 'Pending')], default='pending', max_length=10)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='rides.trip')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
            },
        ),
    ]
