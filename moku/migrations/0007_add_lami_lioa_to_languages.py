# Generated by Django 5.0.3 on 2024-03-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moku', '0006_recipe_post_recipe_recipestep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersettings',
            name='language',
            field=models.CharField(choices=[('en', 'english'), ('lio', 'lami lioa'), ('tok', 'toki pona')], default='en', help_text='what language do you want to use moku.blog in?', max_length=16, verbose_name='language'),
        ),
    ]
