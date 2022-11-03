from django.contrib import admin
from bank.models import BankAccount, SavingPlan, BankAccountLog, ProcessedTransactionId, ScheduledTask


# Register your models here.
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("account_holder", "account_number", "account_balance")


class SavingPlanAdmin(admin.ModelAdmin):
    list_display = ("account_number", "plan_name","deduction_amount", "current_balance", "end_date", "status")


class BankAccountLogAdmin(admin.ModelAdmin):
    list_display = ("receiver", "sender", "amount", "saving_plan", "date_time", "transaction_id")


class ProcessedTransactionIdAdmin(admin.ModelAdmin):
    list_display = ("account", "processed_by_bank_account")


class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ("account", "activation_date", "termination_date")


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(BankAccountLog, BankAccountLogAdmin)
admin.site.register(SavingPlan,SavingPlanAdmin)
admin.site.register(ProcessedTransactionId,ProcessedTransactionIdAdmin)
admin.site.register(ScheduledTask,ScheduledTaskAdmin)


