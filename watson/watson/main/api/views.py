from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.api.serializers import InsurancePackageSerializer
from main.models import InsurancePackage


class InsurancePackageViewset(viewsets.ViewSet):
    queryset = InsurancePackage.objects.all()
    serializer_class = InsurancePackageSerializer

    @action(detail=False, methods=["get"])
    def base(self, request):
        base_packages = self.queryset.filter(is_base=True)

        return Response(self.serializer_class(base_packages, many=True).data)



