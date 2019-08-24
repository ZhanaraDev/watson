from django.core.management import BaseCommand
from django.contrib.auth.models import User

from main.models import ClientCompany, ClientCompanyEmployees


class Command(BaseCommand):
    user_list = [
        {'name': 'Thor', 'surname': 'Odinson', 'username': 'Worthyboy', 'iin': '103456', 'balance': '70000'},
        {'name': 'Tony', 'surname': 'Stark', 'username': 'IronMan', 'iin': '183456', 'balance': '70000'},
        {'name': 'Natasha', 'surname': 'Romanov', 'username': 'BlackWidow', 'iin': '123486', 'balance': '70000'},
        {'name': 'Peter', 'surname': 'Parker', 'username': 'SpiderMan', 'iin': '124456', 'balance': '70000'},
        {'name': 'Naruto', 'surname': 'Uzumaki', 'username': 'Hokage', 'iin': '123256', 'balance': '70000'},
        {'name': 'T', 'surname': 'Challa', 'username': 'BlackPanther', 'iin': '123416', 'balance': '70000'},
        {'name': 'Harry', 'surname': 'Osborn', 'username': 'TheGoblin', 'iin': '123423', 'balance': '70000'},
        {'name': 'Mary', 'surname': 'Jane', 'username': 'MJ', 'iin': '123465', 'balance': '70000'},
    ]

    def handle(self, *args, **options):
        client_company = ClientCompany.objects.create(
            name='ChocoFamily',
            money_paid=500000
        )

        for user in self.user_list:
            if not User.objects.filter(username=user['username']).exists():
                user_ = User.objects.create(username=user['username'], password='1234')

                ClientCompanyEmployees.objects.create(
                    user=user_, name=user['name'],
                    surname=user['surname'],
                    balance=user['balance'],
                    iin=user['iin'],
                    company=client_company,
                )