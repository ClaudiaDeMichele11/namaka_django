# Generated by Django 3.2 on 2021-05-05 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('namaka_admin', '0004_utente_tempo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sorso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_sorso', models.DateField()),
                ('utente', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='namaka_admin.utente')),
            ],
        ),
    ]