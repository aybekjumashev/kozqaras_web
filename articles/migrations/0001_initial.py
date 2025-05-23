# Generated by Django 5.2 on 2025-04-23 12:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Ataması')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Silteme (slug)')),
                ('content', models.TextField(verbose_name='Mazmunı')),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='article_images/', verbose_name='Tiykarǵı Súwret')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Baspa etilgen sáne')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Jaratılǵan sáne')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Jańalanǵan sáne')),
            ],
            options={
                'verbose_name': 'Maqala',
                'verbose_name_plural': 'Maqalalar',
                'ordering': ['-published_date'],
            },
        ),
    ]
