# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0013_auto_20150608_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.CharField(max_length=255, verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Contact message',
                'verbose_name_plural': 'Contact messages',
            },
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(unique=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='token',
            field=models.CharField(verbose_name='Token', max_length=64, editable=False),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='valid',
            field=models.BooleanField(default=False, verbose_name='Valid'),
        ),
    ]
