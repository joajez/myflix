# Generated by Django 4.1.7 on 2023-03-24 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myflixapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='genre_id',
            new_name='external_genre_id',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='movie_id',
            new_name='external_movie_id',
        ),
    ]
