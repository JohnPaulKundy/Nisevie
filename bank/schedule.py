from datetime import date, datetime
from time import strptime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import SavingPlan, BankAccount, ScheduledTask


def plan_activator(activation_date):
    plans = SavingPlan.objects.filter(start_date=activation_date)
    for plan in plans:
        plan.status = True
        plan.save()


def plan_terminator(termination_date):
    plans = SavingPlan.objects.filter(end_date=termination_date)
    for plan in plans:
        plan.status = False
        plan.save()
        account = BankAccount.objects.get(account_number=int(str(plan.account_number)))
        account.account_balance += plan.current_balance
        account.save()


def activate_plan_on(activation_date):
    scheduler = BackgroundScheduler()
    par_s = activation_date.split('-')
    activation_exec_date = date(int(par_s[0]), int(par_s[1]), int(par_s[2]))
    scheduler.add_job(plan_activator, args=[activation_date], trigger='date', run_date=activation_exec_date,
                      misfire_grace_time=10)
    scheduler.start()


def terminate_plan_on(termination_date):
    scheduler = BackgroundScheduler()
    par_t = termination_date.split('-')
    termination_exec_date = date(int(par_t[0]), int(par_t[1]), int(par_t[2]))
    scheduler.add_job(plan_terminator, args=[termination_date], trigger='date', run_date=termination_exec_date,
                      misfire_grace_time=10)
    scheduler.start()


def initialize_tasks():
    account_schedules = ScheduledTask.objects.all()
    schedule_count = len(account_schedules)
    if schedule_count > 0:
        for task in account_schedules:
            today = strptime(str(datetime.now().date()), '%Y-%m-%d').tm_yday
            start_date = strptime(task.activation_date, '%Y-%m-%d').tm_yday
            end_date = strptime(task.termination_date, '%Y-%m-%d').tm_yday
            if (start_date - today) > 0:
                activate_plan_on(task.activation_date)
                terminate_plan_on(task.termination_date)
            elif (end_date - today) > 0:
                terminate_plan_on(task.termination_date)


