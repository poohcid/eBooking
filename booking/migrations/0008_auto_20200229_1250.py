# Generated by Django 3.0.3 on 2020-02-29 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20200229_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('No', 'ไม่อนุมัติ'), ('yes', 'อนุมัติ')], default=None, max_length=100, null=True),
        ),
    ]