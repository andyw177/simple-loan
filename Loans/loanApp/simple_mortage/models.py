from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """Extended user profile with financial information"""
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    phone_number    = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth   = models.DateField(blank=True, null=True)
    credit_score    = models.PositiveIntegerField(null=True, blank=True)
    dto_ratio       = models.PositiveIntegerField( null=True, blank=True)

    def __str__(self):
        return self.username

class Lender(models.Model):
    """
    Lender model representing financial institutions
    """
    name = models.CharField(max_length=100)
    tid = models.CharField(max_length=100)
    
    
    
    def __str__(self):
        return self.name

class Property(models.Model):
    """
    Property model for which loans can be applied
    """
    address = models.CharField(max_length=255)
    property_type_choices = [
        ('SFH', 'Single Family Home'),
        ('CONDO', 'Condominium'),
        ('TOWNHOUSE', 'Townhouse'),
        ('MULTI', 'Multi-Family'),
        ('OTHER', 'Other')
    ]
    property_type = models.CharField(max_length=10, choices=property_type_choices)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)

    
    def __str__(self):
        return f"{self.address}, {self.property_type}, Estimated Value: {self.estimated_value}, Purchase Price:   {self.purchase_price}"
    
    

class Application(models.Model):
    """
    Loan application model connecting users, properties, and lenders
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DECLINED', 'Declined'),
        ('APPROVED', 'Approved'),
 
    ]
    
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    lender = models.ForeignKey(Lender, on_delete=models.CASCADE, related_name='applications')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='applications')
   
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_term_years = models.PositiveIntegerField()
    down_payment = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    application_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Application #{self.id} - {self.applicant.username} - {self.status}"
    
class PreQualCriteria(models.Model):
    lender =  models.OneToOneField(Lender, on_delete=models.CASCADE)
    loan_amount = models.PositiveIntegerField()
    credit_score = models.PositiveIntegerField()
    annual_income = models.PositiveIntegerField()
    dto_ratio = models.PositiveIntegerField()
    down_payment = models.PositiveIntegerField()


    def __str__(self):
        return self.lender.name
    