# Generated by Django 5.0.6 on 2024-06-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('fashion', 'Fashion'), ('home_appliances', 'Home Appliances'), ('books', 'Books'), ('toys', 'Toys'), ('sports', 'Sports'), ('beauty', 'Beauty')], default='Electronics', max_length=25),
        ),
    ]
