# Generated by Django 3.1.2 on 2021-06-09 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('namaka_admin', '0006_auto_20210609_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codicesconto',
            name='utente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]