# Generated by Django 2.0.4 on 2018-04-17 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0002_auto_20180406_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=175, null=True, verbose_name='Nome')),
                ('device_id', models.CharField(max_length=275, verbose_name='Device ID')),
                ('type_a', models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo A')),
                ('type_b', models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo B')),
                ('type_c', models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo C')),
                ('type_d', models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo D')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_device', to='customers.Organization')),
            ],
            options={
                'verbose_name': 'Dispositivo',
                'verbose_name_plural': 'Dispositivos',
            },
        ),
    ]
