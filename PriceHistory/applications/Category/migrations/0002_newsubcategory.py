# Generated by Django 4.2.2 on 2023-07-04 16:05

from django.db import migrations, models
import django.db.models.deletion


def copy_data(apps, schema_editor):
    OldModel = apps.get_model('Subcategory', 'Subcategory')
    NewModel = apps.get_model('Category', 'NewSubcategory')
    for old_model in OldModel.objects.all():
        NewModel.objects.create(
            subcategory_name=old_model.subcategory_name,
            category=old_model.category)


class Migration(migrations.Migration):
    dependencies = [
        ('Category', '0001_initial'),
    ]

    operations = [migrations.CreateModel(
        name='NewSubcategory',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('subcategory_name', models.CharField(unique=True)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Category.category')),
        ],
        options={
            'db_table': 'new_subcategory',
        },
    ),
        migrations.RunPython(copy_data),
    ]