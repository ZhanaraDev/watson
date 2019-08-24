from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.api.serializers import InsurancePackageSerializer, CategorySerializer
from main.models import InsurancePackage, Category, InsurancePackageCategories


class InsurancePackageViewset(viewsets.ModelViewSet):
    queryset = InsurancePackage.objects.all()
    serializer_class = InsurancePackageSerializer

    @action(detail=True, methods=['post'])
    def create_package(self, requests):
        body = requests.data
        package_name = body.get('package_name')
        category_list = body.get('category_list')
        package = InsurancePackage.objects.create(package_name=package_name)
        for category in Category.objects.filter(pk__in=category_list).distinct():
            InsurancePackageCategories.objects.create(category=category, package=package)

    @action(detail=False)
    def base(self, request):
        base_packages = self.queryset.filter(is_base=True)
        return Response(self.serializer_class(base_packages, many=True).data)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


