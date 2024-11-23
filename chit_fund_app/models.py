# from django.db import models

# Create your models here.
from django.db import models
class ChitGroup(models.Model):
    group_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    months = models.PositiveIntegerField()  
    members_count = models.PositiveIntegerField() 

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    ticket_number = models.CharField(max_length=100, null=True, blank=True) 
    group_name = models.ForeignKey(ChitGroup, on_delete=models.CASCADE,related_name="subscribers", null=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    group_name = models.ForeignKey(ChitGroup, on_delete=models.CASCADE)  # Corrected field name
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=255, blank=True)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Cheque', 'Cheque'), ('Online', 'Online')])
    installment_number = models.IntegerField(null=True, blank=True)
    installment_month =  models.CharField(max_length=7, null=True, blank=True)
    arrears = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    future_dues = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_penalty = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cheque_details = models.TextField(null=True, blank=True)
    dividend_allowed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_forfeited = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_decided = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    receiving_clerk_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Payment {self.id} - {self.subscriber.name}"


