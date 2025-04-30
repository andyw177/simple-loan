from rest_framework import serializers
from .models import UserProfile, Lender, Property, Application,PreQualCriteria

from django.contrib.auth import get_user_model

User = get_user_model()

# for login users
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','annual_income', 'credit_score','dto_ratio','password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }
    
    def create(self, validated_data):
        """Create and return a new user"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update a user, correctly handling the password"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class LenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lender
        fields = '__all__'
        read_only_fields = ['id']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id']

class PrequalCriteriaSerializer(serializers.ModelSerializer):
    lender_name = serializers.ReadOnlyField(source='lender.name')
    
    class Meta:
        model = PreQualCriteria
        fields = ['id', 'lender', 'lender_name', 'credit_score', 'dto_ratio',
                'loan_amount', 'down_payment','annual_income']
        read_only_fields = ['id', 'lender_name']

class PrequalificationApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.ReadOnlyField(source='applicant.get_full_name')
    lender_name = serializers.ReadOnlyField(source='lender.name')
    property_address = serializers.ReadOnlyField(source='property.__str__')
    
    class Meta:
        model = Application
        fields = ['id', 'applicant', 'applicant_name', 'lender', 'lender_name', 
                 'property', 'property_address', 'application_date',
                 'loan_amount', 'down_payment', 'loan_term_years','status']
        read_only_fields = ['id', 'applicant_name', 'lender_name', 'property_address', 
                          'application_date','status']

