# Generated by Django 5.0 on 2023-12-14 18:53

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('unique_id', models.AutoField(primary_key=True, serialize=False, verbose_name='уникальный id клиента')),
                ('phone_number', models.CharField(max_length=11, verbose_name='номер телефона клиента')),
                ('operator_code', models.CharField(max_length=10, verbose_name='код мобильного оператора')),
                ('tag', models.CharField(max_length=255, verbose_name='тэг')),
                ('time_zone', models.CharField(max_length=255, verbose_name='часовой пояс')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Уникальный id рассылки')),
                ('launch_date_time', models.DateTimeField(verbose_name='дата и время запуска рассылки')),
                ('text', models.TextField(verbose_name='текст сообщения для доставки клиенту')),
                ('client_filter', models.CharField(max_length=255, verbose_name='фильтр свойств клиентов')),
                ('end_date_time', models.DateTimeField(verbose_name='дата и время окончания рассылки')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('unique_id', models.AutoField(primary_key=True, serialize=False, verbose_name='уникальный id сообщения')),
                ('create_date_time', models.DateTimeField(verbose_name='дата и время создания (отправки)')),
                ('status', models.CharField(choices=[('Not sent', 'Not sent'), ('In progress', 'In progress'), ('Sent', 'Sent')], max_length=255, verbose_name='статус отправки')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.client', verbose_name='id клиента, которому отправили')),
                ('mailing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.mailing', verbose_name='id рассылки, в рамках которой было отправлено сообщение')),
            ],
        ),
    ]
