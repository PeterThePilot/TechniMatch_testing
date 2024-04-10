# Generated by Django 5.0.3 on 2024-04-01 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_usercourseranking_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourseranking',
            name='ranking',
            field=models.IntegerField(choices=[(0, 'Have not taken yet'), (1, 'Do not like at all'), (2, 'Do not like'), (3, 'Neutral'), (4, 'Like'), (5, 'Like a lot')], default=0),
        ),
    ]
