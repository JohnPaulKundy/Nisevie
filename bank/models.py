import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


def get_the_full_name(self):
    return self.get_full_name()


User.add_to_class("__str__", get_the_full_name)


# Create your models here.
class BankAccount(models.Model):
    account_holder = models.ForeignKey(to=User, on_delete=models.CASCADE)
    account_number = models.BigIntegerField(verbose_name="account number")
    account_balance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.account_number}'


class SavingPlan(models.Model):
    account_number = models.ForeignKey(to=BankAccount, on_delete=models.CASCADE)
    sender_account = models.BigIntegerField()
    plan_name = models.CharField(max_length=30)
    deduction_amount = models.FloatField(null=False)
    current_balance = models.FloatField(default=0)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.account_number}'


class BankAccountLog(models.Model):
    receiver = models.ForeignKey(to=BankAccount, on_delete=models.CASCADE)
    sender = models.BigIntegerField()
    saving_plan = models.CharField(max_length=30, null=True)
    amount = models.FloatField(default=0)
    date_time = models.DateTimeField(default=now)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f'{self.receiver}'


class ProcessedTransactionId(models.Model):
    account = models.ForeignKey(to=BankAccount, on_delete=models.CASCADE)
    processed_by_bank_account = models.UUIDField(null=True)

    def __str__(self):
        return f'{self.account}'


class ScheduledTask(models.Model):
    account = models.ForeignKey(to=BankAccount, on_delete=models.CASCADE)
    activation_date = models.CharField(max_length=30)
    termination_date = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.account}'

