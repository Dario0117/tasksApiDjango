# Generated by Django 2.0.7 on 2018-07-29 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20180728_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=500)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.User')),
            ],
        ),
    ]
