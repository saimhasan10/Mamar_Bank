from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE


class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount, related_name="transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Admin approval flag
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.account.user.username} - {self.get_transaction_type_display()} - ${self.amount}"
