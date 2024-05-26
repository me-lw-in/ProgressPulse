# Generated by Django 5.0.4 on 2024-05-26 07:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceData',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('section', models.CharField(default='0', max_length=10, null=True)),
                ('attendance_date', models.DateField()),
                ('period', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('morning', 'Morning'), ('afternoon', 'Afternoon')], default='0', max_length=10)),
                ('attendance_status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent')], default='A', max_length=1)),
                ('subject_type', models.CharField(max_length=100, null=True)),
                ('sem', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=1)),
                ('registration_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to=settings.AUTH_USER_MODEL)),
                ('subject_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='academics.subject')),
            ],
        ),
    ]
