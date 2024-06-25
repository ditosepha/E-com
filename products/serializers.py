from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['rating', 'num_reviews', 'owner']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is not None:
            validated_data['owner'] = request.user

        return super(ProductSerializer, self).create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"