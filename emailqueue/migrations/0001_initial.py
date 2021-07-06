# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QueuedMail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('sender', models.EmailField(default=b'valid@email.com', max_length=254, verbose_name='From')),
                ('date', models.DateField(verbose_name='Date')),
                ('sent', models.DateTimeField(verbose_name='Sent', null=True, editable=False)),
                ('subject', models.CharField(max_length=128, verbose_name='Subject')),
                ('content', models.TextField(verbose_name='Content')),
                ('errors', models.CharField(verbose_name='Error', max_length=256, editable=False)),
                ('to', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Queued Email',
                'verbose_name_plural': 'Queued Emails',
            },
        ),
    ]
