from collections import OrderedDict
from datetime import timedelta, datetime
from datetime import time as dt_time

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.api.serializers import InsurancePackageSerializer, CategorySerializer, ClientCompanyEmployeesSerializer, \
    ServiceProviderSerializer
from main.models import InsurancePackage, Category, InsurancePackageCategories, ClientCompanyEmployees, ServiceProvider, \
    ServiceProviderSchedule, Appointment, WEEK_DICT


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


class ServiceProviderViewset(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceProviderSerializer

    @action(detail=False)
    def available(self, request):
        package = ClientCompanyEmployees.objects.filter(
            user=request.user).first().insurance_package

        categories = Category.objects.filter(
            id__in=InsurancePackageCategories.objects.filter(
                package=package
            ).distinct('category').values('category__id'))

        sps = ServiceProvider.objects.filter(categories__in=categories)
        return Response(self.serializer_class(sps, many=True).data)


class AppointmentViewSet(viewsets.ViewSet):
    queryset = Appointment.objects.none()
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_start_end_days_of_week(today):
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end

    @action(detail=True)
    def schedule(self, request, pk):
        service_provider = ServiceProvider.objects.get(id=pk)
        schedule = ServiceProviderSchedule.objects.filter(service_provider=service_provider)
        start_day, end_day = self.get_start_end_days_of_week(datetime.today())
        appointments = Appointment.objects.filter(
            service_provider=service_provider,
            date__gte=start_day,
            date__lte=end_day,
        )
        print(appointments)
        schedule_dict = {}
        for s in schedule:
            k = WEEK_DICT[s.day]
            schedule_dict[k] = []
            appointments_list = appointments.filter(
                week_day=s.day
            ).order_by('time').values_list('time', flat=True)
            st = s.time_start.hour
            end = s.time_end.hour
            time_slots = list(range(st, end+1))

            for appoint in appointments_list:
                if appoint.hour in time_slots:
                    time_slots.remove(appoint.hour)

            schedule_dict[k] = time_slots
        sorted_schedule = OrderedDict(sorted(schedule_dict.items(), key=lambda t: t[0]))
        return Response(sorted_schedule)

    @action(detail=True, methods=["post"])
    def appoint(self, request, pk):
        week_dict = {v: k for k, v in WEEK_DICT.items()}

        date = datetime.strptime(request.data.get('date'), "%Y/%m/%d") #2019/08/05 y m d
        time = dt_time(hour=int(request.data.get('time'))) #int
        week_day = week_dict[int(request.data.get('week_day'))] #int 1-7

        employee = ClientCompanyEmployees.objects.get(user=request.user)
        service_provider = ServiceProvider.objects.get(id=pk)

        if employee.balance - service_provider.visit_cost >= 0:
            employee.balance -= service_provider.visit_cost
            employee.save()
            if not Appointment.objects.filter(
                    week_day=week_day,
                    date=date, time=time,
                    service_provider=service_provider).exists():

                Appointment.objects.create(
                    employee=employee,
                    service_provider=service_provider,
                    week_day=week_day,
                    date=date,
                    time=time
                )
            else:
                return Response('Это время занято', status=400)

        else:
            return Response('Недостаточно баланса', status=400)
        return Response(status=200)
