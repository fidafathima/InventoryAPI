# Generated by Django 5.0.6 on 2024-11-17 13:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0005_remove_paymentmethod_card_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
