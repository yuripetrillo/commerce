# Generated by Django 4.2.3 on 2023-09-16 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_categoryname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='startingbid',
            new_name='startingprice',
        ),
    ]
