from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from main.api.serializers import InsurancePackageSerializer, CategorySerializer, ClientCompanyEmployeesSerializer
from main.models import InsurancePackage, Category, InsurancePackageCategories, ClientCompanyEmployees


class InsurancePackageViewset(viewsets.ModelViewSet):
    queryset = InsurancePackage.objects.all()
    serializer_class = InsurancePackageSerializer
    authentication_classes = (TokenAuthentication,)

    @action(detail=True, methods=['post'])
    def create_package(self, request):
        user = request.user
        body = request.data
        package_name = body.get('package_name')
        category_list = body.get('category_list')
        package = InsurancePackage.objects.create(package_name=package_name)
        for category in Category.objects.filter(pk__in=category_list).distinct():
            InsurancePackageCategories.objects.create(category=category, package=package)
        client_employee = ClientCompanyEmployees.objects.get(user=user)
        client_employee.package = package
        client_employee.save()

        return Response(self.serializer_class(instance=package).data)


    @action(detail=False)
    def base(self, request):
        base_packages = self.queryset.filter(is_base=True)
        return Response(self.serializer_class(base_packages, many=True).data)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProfileViewset(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = ClientCompanyEmployees.objects.all()
    serializer_class = ClientCompanyEmployeesSerializer

    @action(detail=False)
    def show(self, request):
        user = request.user
        instance = ClientCompanyEmployees.objects.get(user=user)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)
