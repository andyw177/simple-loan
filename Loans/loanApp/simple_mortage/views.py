
# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from  .models import *
from  .serializer import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """Only allow users to see their own profile"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

class LenderViewSet(viewsets.ModelViewSet):
    queryset = Lender.objects.all()
    serializer_class = LenderSerializer
    def get_queryset(self):
        return Property.objects.all()
       

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    def get_queryset(self):
        return Property.objects.all()
       

class PrequalificationCriteriaViewSet(viewsets.ModelViewSet):
    queryset = PreQualCriteria.objects.all()
    serializer_class = PrequalCriteriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by lender if specified"""
        queryset = PreQualCriteria.objects.all()
        lender_id = self.request.query_params.get('lender', None)
        if lender_id:
            queryset = queryset.filter(lender_id=lender_id)
        return queryset

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = PrequalificationApplicationSerializer
    
    def get_queryset(self):
        """Users can only see their own applications, staff can see all"""
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(applicant=self.request.user)
    
    def perform_create(self, serializer):
        """Set the applicant to the current user"""
        serializer.save(applicant=self.request.user)
    
    # prequalify
    @action(detail=True, methods=['GET'])
    def prequalify(self, request, pk=None):
        """
        Endpoint to prequalify an application.
        For now, just randomly returns 'yes' or 'no' without any actual criteria.
        """
        application = Application.objects.get(id=pk)
        
        profile = User.objects.get(id=application.applicant.id)
        lender = application.lender
        criteria = PreQualCriteria.objects.filter(lender_id= lender.id).first()

        # check criteria max loan amount, min credit score, min income, min dto_ratio, min downpayment

        if(criteria.loan_amount >= application.loan_amount and criteria.credit_score <= profile.credit_score 
           and criteria.annual_income <= profile.annual_income and criteria.dto_ratio <= profile.annual_income and criteria.down_payment <= application.down_payment):
           application.status = 'Approved'
        else:
            application.status = 'Denied'
            
        application.save()

        
        return Response(application.status)
