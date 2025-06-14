# transactions/admin.py

from django.contrib import admin
from .models import Transaction
from transactions.utils import send_transaction_email  # updated import


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "amount",
        "balance_after_transaction",
        "transaction_type",
        "is_approved",
        "timestamp",
    ]
    list_filter = ["is_approved", "transaction_type"]
    actions = ["approve_transactions"]

    def approve_transactions(self, request, queryset):
        for obj in queryset:
            if not obj.is_approved:
                obj.is_approved = True
                account = obj.account

                if obj.transaction_type == 1:  # DEPOSIT
                    account.balance += obj.amount
                elif obj.transaction_type == 2:  # WITHDRAWAL
                    account.balance -= obj.amount
                elif obj.transaction_type == 3:  # LOAN
                    account.balance += obj.amount

                account.save(update_fields=["balance"])
                obj.balance_after_transaction = account.balance
                obj.save()

                send_transaction_email(
                    obj.account.user,
                    obj.amount,
                    obj.get_transaction_type_display(),  # dynamic name like "Deposit"
                    "Transaction Approved",
                    "transactions/admin_email.html",
                )

        self.message_user(request, "Selected transactions approved and processed.")

    approve_transactions.short_description = "Approve selected pending transactions"

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            account = obj.account

            if obj.transaction_type == 1:
                account.balance += obj.amount
            elif obj.transaction_type == 2:
                account.balance -= obj.amount
            elif obj.transaction_type == 3:
                account.balance += obj.amount

            account.save(update_fields=["balance"])
            obj.balance_after_transaction = account.balance

            send_transaction_email(
                obj.account.user,
                obj.amount,
                obj.get_transaction_type_display(),
                "Transaction Approved",
                "transactions/admin_email.html",
            )

        super().save_model(request, obj, form, change)
