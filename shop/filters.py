import django_filters
from django import forms

from .models import Product, Category

STATUS_CHOICES = (
    (True, 'Available'),
    (False, 'Not available'),
)

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    available = django_filters.MultipleChoiceFilter(choices = STATUS_CHOICES,
    	widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        fields = ['category', 'available']