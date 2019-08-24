from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.api.serializers import InsurancePackageSerializer, CategorySerializer, ClientCompanyEmployeesSerializer, \
    ServiceProviderSerializer
from main.models import InsurancePackage, Category, InsurancePackageCategories, ClientCompanyEmployees, ServiceProvider


class InsurancePackageViewset(viewsets.ModelViewSet):
    queryset = InsurancePackage.objects.all()
    serializer_class = InsurancePackageSerializer
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['post', ])
    def assign_package(self, request):
        user = request.user
        package_id = request.data.get('package')

        package = InsurancePackage.objects.get(id=package_id)

        ClientCompanyEmployees.objects.filter(
            user=user
        ).update(insurance_package=package)

        return Response(self.serializer_class(instance=package).data)

    @action(detail=False, methods=['post', ])
    def create_package(self, request):
        body = request.data
        package_name = body.get('package_name')
        category_list = body.get('category_list').split(',')
        print("cats", category_list)
        package = InsurancePackage.objects.create(package_name=package_name)
        for category in Category.objects.filter(pk__in=category_list).distinct():
            InsurancePackageCategories.objects.create(category=category, package=package)

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
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def show(self, request):
        user = request.user
        instance = ClientCompanyEmployees.objects.get(user=user)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class ServiceProviderViewset(viewsets.ViewSet):
    queryset = ClientCompanyEmployees.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceProviderSerializer

    @action(detail=False)
    def available(self, request):
        package = self.queryset.filter(
            user=request.user).first().insurance_package

        categories = Category.objects.filter(
            id__in=InsurancePackageCategories.objects.filter(
                package=package
            ).distinct('category').values('category__id'))

        sps = ServiceProvider.objects.filter(categories__in=categories)
        return Response(self.serializer_class(sps, many=True).data)


