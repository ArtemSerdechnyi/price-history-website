# Generated by Django 4.2.2 on 2023-07-04 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
        ('Category', '0003_alter_newsubcategory_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewSubcategory',
            new_name='Subcategory',
        ),
        migrations.AlterModelTable(
            name='subcategory',
            table='subcategory',
        ),
    ]
