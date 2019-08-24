from rest_framework import serializers

from main.models import Category, InsurancePackage, InsurancePackageCategories


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class InsurancePackageSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = InsurancePackage
        fields = ('package_name', 'categories', )

    def get_categories(self, obj):
        cats = Category.objects.filter(id__in=InsurancePackageCategories.objects.filter(
            package=obj).distinct('category').values('category__id'))
        cats = CategorySerializer(cats, many=True)
        return cats.data
