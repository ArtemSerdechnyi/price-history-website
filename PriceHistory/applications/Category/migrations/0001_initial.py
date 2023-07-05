# Generated by Django 4.2.2 on 2023-07-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(unique=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
    ]
