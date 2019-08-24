from rest_framework import serializers

from main.models import Category, InsurancePackage, InsurancePackageCategories, ClientCompanyEmployees, ServiceProvider


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class InsurancePackageSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = InsurancePackage
        fields = ('id', 'package_name', 'categories', )

    def get_categories(self, obj):
        cats = Category.objects.filter(id__in=InsurancePackageCategories.objects.filter(
            package=obj).distinct('category').values('category__id'))
        cats = CategorySerializer(cats, many=True)
        return cats.data


class ClientCompanyEmployeesSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return int(obj.balance)

    class Meta:
        model = ClientCompanyEmployees
        fields = '__all__'


class ServiceProviderSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    visit_cost = serializers.SerializerMethodField()

    def get_position(self, obj):
        positions = {
            'dentist': u'Дантист',
            'therapist': u'Терапевт',
            'psychologist': u'Психолог',
            'surgeon': u'Хирург',
            'gynecologist': u'Гинеколог',
            'nurse': u'Мед. сестра',
            'neurologist': u'Невропатолог'
        }
        return positions.get(obj.position, obj.position)

    def get_visit_cost(self, obj):
        return int(obj.visit_cost)

    class Meta:
        model = ServiceProvider
        fields = ('id', 'name', 'surname', 'avatar', 'position', 'visit_cost')
