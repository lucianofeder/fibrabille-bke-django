# Generated by Django 4.0 on 2021-12-22 17:25

from django.db import migrations, models
import django.db.models.deletion
import user.services.user_private


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=True)),
                ('is_sales_rep', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('extra_info', models.CharField(max_length=256)),
                ('blocked', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserPrivate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('birthdate', models.DateField()),
                ('cpf', models.CharField(max_length=14, validators=[user.services.user_private.Validator.cpf])),
                ('mother_name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]