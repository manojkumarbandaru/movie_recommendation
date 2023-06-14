# Generated by Django 4.2.2 on 2023-06-14 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relateduser',
            name='related_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_to_user', to='recommend.user'),
        ),
        migrations.AlterField(
            model_name='relateduser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_user', to='recommend.user'),
        ),
    ]