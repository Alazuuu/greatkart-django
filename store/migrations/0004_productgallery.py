# Generated by Django 3.2.8 on 2022-02-24 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_reviewrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=255, upload_to='store/products')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'productgallery',
                'verbose_name_plural': 'product gallery',
            },
        ),
    ]
