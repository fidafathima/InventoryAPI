# Generated by Django 5.0.6 on 2024-06-10 08:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='products',
            name='product_color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='InventoryApp.color'),
        ),
        migrations.AlterField(
            model_name='products',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='InventoryApp.size'),
        ),
    ]