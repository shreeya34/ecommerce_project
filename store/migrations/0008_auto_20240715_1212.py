# Generated by Django 3.2.16 on 2024-07-15 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_productcolor_productsize'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('color', models.CharField(max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
            ],
        ),
        migrations.RemoveField(
            model_name='productsize',
            name='product',
        ),
        migrations.DeleteModel(
            name='ProductColor',
        ),
        migrations.DeleteModel(
            name='ProductSize',
        ),
    ]
