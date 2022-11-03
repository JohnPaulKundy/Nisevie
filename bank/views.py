from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from bank.engines import saving_plan_engine, create_plan_engine, cal_rem_days
from bank.models import BankAccount, SavingPlan, BankAccountLog
from datetime import datetime, timedelta


# Create your views here.
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
            return redirect('/home')
        except:
            return render(request, 'login.html', context={'error': 'wrong username or password !!!'})
    return render(request, 'login.html')


def registration_view(request):
    if request.POST:
        username = request.POST['username']
        account = request.POST['account_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name)
        user.is_staff = False
        user.save()
        bank_account = BankAccount(account_holder=user, account_number=account)
        bank_account.save()
        return redirect('login')
    return render(request, 'registration.html')


@login_required(login_url='login')
def plan_list_view(request):
    total_balance = 0
    account = BankAccount.objects.get(account_holder=request.user)
    plans = SavingPlan.objects.all().filter(account_number=account)
    plans_count = len(plans)
    if plans_count > 0:
        for plan in plans:
            total_balance += plan.current_balance
        context = {'plans': plans, 'plans_count': plans_count, 'total_balance': total_balance,
                   'is_terminated': cal_rem_days}
    else:
        context = {'plans': plans, 'plans_count': plans_count}
    return render(request, 'plan_list.html', context)


@login_required(login_url='login')
def home_view(request):
    holder = BankAccount.objects.get(account_holder=request.user)
    context = {'holder': holder}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def plan_manager_view(request):
    plans = SavingPlan.objects.all()
    account = BankAccount.objects.get(account_holder=request.user)
    today = datetime.today().date().strftime('%Y-%m-%d')
    last_date = (timedelta(days=90) + datetime.strptime(str(datetime.today().date()), '%Y-%m-%d')).strftime('%Y-%m-%d')
    context = {'plans': plans, 'today': today, 'last_date': last_date}
    if request.POST:
        sender_account = request.POST['sender_account']
        plan_name = request.POST['plan_name']
        deduction_amount = request.POST['deduction_amount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        create_plan_engine(account, sender_account, plan_name, deduction_amount, start_date, end_date, today)
        return redirect('plan_manager')
    return render(request, 'plan_manager.html', context)


@login_required(login_url='login')
def send_funds_view(request):
    if request.POST:
        try:
            sender = request.POST['sender']
            receiver = request.POST['receiver_account']
            amount = request.POST['amount']
            try:
                account = BankAccount.objects.get(account_number=receiver)
                context = {'receiver': account, 'sender': sender, 'amount': amount}
                return render(request, 'send_fund_confirmation.html', context)
            except:
                return render(request, 'send_fund.html', context={'error': 'Receiving account does not exist'})
        except:
            sender = request.POST['sender']
            receiver = request.POST['receiver']
            amount = request.POST['amount']
            account = BankAccount.objects.get(account_number=receiver)
            logs = BankAccountLog(receiver=account, sender=sender, amount=amount)
            logs.save()
            saving_plan_engine(account, sender, amount)
            return redirect('send_fund')
    return render(request, 'send_fund.html')
