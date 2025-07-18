# Generated by Django 5.2.3 on 2025-07-18 09:25

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='paper_size',
            field=models.CharField(choices=[('a4', 'A4'), ('b5', 'B5')], default='a4', help_text='纸张尺寸', max_length=10),
        ),
        migrations.AlterField(
            model_name='document',
            name='file_path',
            field=models.FileField(help_text='文件存储路径', upload_to=api.models.get_order_document_path),
        ),
        migrations.AlterField(
            model_name='document',
            name='print_sided',
            field=models.CharField(choices=[('single', '单面打印'), ('double', '双面打印'), ('single_double', '封面单面')], default='single', help_text='单双面', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_screenshot',
            field=models.FileField(blank=True, help_text='支付凭证截图', null=True, upload_to=api.models.get_payment_screenshot_path),
        ),
    ]
