# Generated by Django 2.2.24 on 2021-09-30 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coplate', '0004_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='intro',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='defalt_profile_pic.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')], default=None),
        ),
    ]
