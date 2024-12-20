# Generated by Django 5.0.6 on 2024-08-22 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity0', models.CharField(default=1, max_length=15)),
                ('status', models.CharField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='InventoryApp.productdetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
