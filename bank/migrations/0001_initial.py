# Generated by Django 4.1.1 on 2022-11-03 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.BigIntegerField(verbose_name='account number')),
                ('account_balance', models.FloatField(default=0)),
                ('account_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_date', models.CharField(max_length=30)),
                ('termination_date', models.CharField(max_length=30)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='SavingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_account', models.BigIntegerField()),
                ('plan_name', models.CharField(max_length=30)),
                ('deduction_amount', models.FloatField()),
                ('current_balance', models.FloatField(default=0)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('account_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedTransactionId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processed_by_bank_account', models.UUIDField(null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccountLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.BigIntegerField()),
                ('saving_plan', models.CharField(max_length=30, null=True)),
                ('amount', models.FloatField(default=0)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('transaction_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bankaccount')),
            ],
        ),
    ]
