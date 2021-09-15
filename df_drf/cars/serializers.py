from cars.models import *
from rest_framework import serializers


class BrandField(serializers.RelatedField):
    def get_queryset(self):
        return Brand.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            brand = Brand.objects.get(name=data)
        except:
            raise serializers.ValidationError(f'Brand not found {data}')
        return brand


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    num_of_cars = serializers.SerializerMethodField('get_num_of_cars')

    class Meta:
        model = Brand
        fields = ('id', 'name', 'num_of_cars', 'created', 'created_at')
    
    def get_num_of_cars(self, brand):
        return brand.num_of_cars


class CarSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandField(many=False, read_only=False, required=False)

    class Meta:
        model = Car
        fields = ('id', 'name', 'height', 'width', 'brand')
