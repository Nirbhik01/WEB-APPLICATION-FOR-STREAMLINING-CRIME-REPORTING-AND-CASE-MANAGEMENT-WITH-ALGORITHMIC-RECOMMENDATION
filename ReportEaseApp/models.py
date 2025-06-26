from django.db import models
from Case.models import Case
from userauths.models import Citizen,Investigator


class Notification(models.Model):
    NOTIFICATION_STATUS = [
        ('UNREAD', 'Unread'),
        ('READ', 'Read')
    ]

    belongs_to_citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True, blank=True, default=None)
    belongs_to_investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE, null=True, blank=True, default=None)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='UNREAD')

    
    class Meta:
        unique_together = [
            ('belongs_to_citizen', 'belongs_to_investigator', 'case', 'message'),
            ('belongs_to_citizen', 'belongs_to_investigator', 'case', 'message')
        ]
    
    def __str__(self):
        return f"Notification for {self.case.case_id}-{self.case.case_title}-{self.timestamp}"
    

class Payment(models.Model):
    PAYMENT_PROVIDERS = [
        ('STRIPE', 'Stripe'),
        ('PAYPAL', 'PayPal')
    ]
    
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE,default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_provider = models.CharField(max_length=10, choices=PAYMENT_PROVIDERS,default='PAYPAL')
    payment_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.user} - {self.amount}"

    class Meta:
        ordering = ['-timestamp']
# Create your models here.
