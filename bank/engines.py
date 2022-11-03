from datetime import datetime
from time import strptime
from django.db.models.signals import post_save
from django.dispatch import receiver
from bank.models import SavingPlan, BankAccountLog, ProcessedTransactionId, BankAccount, ScheduledTask
from bank.schedule import activate_plan_on, terminate_plan_on


def cal_rem_days(end_date):
    today = strptime(str(datetime.now().date()), '%Y-%m-%d').tm_yday
    ending_date = strptime(str(end_date), '%Y-%m-%d').tm_yday
    rem_days = ending_date-today
    if rem_days > 0:
        return False
    else:
        return True


def create_plan_engine(*args):
    schedule = ScheduledTask(account=args[0], activation_date=args[4], termination_date=args[5])
    schedule.save()
    if args[4] == args[6]:
        new_plan = SavingPlan(account_number=args[0], sender_account=args[1], plan_name=args[2],
                              deduction_amount=args[3], start_date=args[4], end_date=args[5],
                              status=True)
        new_plan.save()
        terminate_plan_on(args[5])
    else:
        new_plan = SavingPlan(account_number=args[0], sender_account=args[1], plan_name=args[2],
                              deduction_amount=args[3], start_date=args[4], end_date=args[5])
        new_plan.save()
        activate_plan_on(args[4])
        terminate_plan_on(args[5])


def saving_plan_engine(self, sender, amount):
    plans = SavingPlan.objects.all().filter(account_number=self, sender_account=sender)
    for plan in plans:
        if plan.status:
            if plan.deduction_amount >= float(str(amount)):
                log = BankAccountLog(receiver=self, sender=sender, saving_plan=plan.plan_name,
                                     amount=amount)
            else:
                log = BankAccountLog(receiver=self, sender=sender, saving_plan=plan.plan_name,
                                     amount=plan.deduction_amount)
            log.save()
        else:
            pass


def main_bank_engine(self):
    for log in self:
        log_receiver = int(str(log.receiver))
        account = BankAccount.objects.get(account_number=log_receiver)
        balance = account.account_balance
        processed_log = ProcessedTransactionId(account=account, processed_by_bank_account=log.transaction_id)
        processed_log.save()
        if log.saving_plan is None:
            balance += log.amount
            account.account_balance = str(balance)
        else:
            plan = SavingPlan.objects.get(plan_name=log.saving_plan)
            plan_balance = plan.current_balance
            plan_balance += log.amount
            plan.current_balance = str(plan_balance)
            plan.save()
            balance -= log.amount
            account.account_balance = str(balance)
        account.save()


@receiver(post_save, sender=BankAccountLog)
def bank_engine_caller(sender, **kwargs):
    logs = BankAccountLog.objects.all()
    processed_logs = ProcessedTransactionId.objects.all()
    if len(processed_logs) == 0:
        main_bank_engine(logs)
    else:
        for processed_log in processed_logs:
            logs = logs.exclude(transaction_id=processed_log.processed_by_bank_account)
        main_bank_engine(logs)
