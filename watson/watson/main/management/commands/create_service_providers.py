from django.core.management import BaseCommand
from django.contrib.auth.models import User

from main.models import ClientCompany, ClientCompanyEmployees, ServiceProvidingHolding, ServiceProvider, Category


class Command(BaseCommand):
    user_list = [
        {'name': 'Bruce','surname':'Wayne','position': 'dentist','visit_cost':3000,'avatar':'http://beauty-around.com/images/sampledata/Hollywood_Actors/24zac-efron.jpg', 'title': ['Узкий']},
        {'name': 'Clark','surname':'Kent','position': 'therapist','visit_cost':1000,'avatar': 'http://beauty-around.com/images/sampledata/Hollywood_Actors/19rainReinolds.jpg', 'title': ['Диагностические']},
        {'name': 'Felicity','surname': 'Smoak','position': 'psychologist','visit_cost': 6000,'avatar':'http://beauty-around.com/images/sampledata/Hollywood_Actors/Gabriel-Macht4.jpg', 'title': ['Лобарот']},
        {'name': 'Barry','surname': 'Allen','position': 'surgeon','visit_cost': 10000,'avatar': 'http://beauty-around.com/images/sampledata/Hollywood_Actors/8Bred_Pitt.jpg', 'title': ['Узкий']},
        {'name': 'Tobiwan','surname': 'Kenobi','position': 'gynecologist','visit_cost': 1000,'avatar': 'http://beauty-around.com/images/sampledata/Italian_Model/23maria-perrusiItalia2009.jpg', 'title': ['Узкий','Семейный']},
        {'name': 'Dart','surname': 'Veider','position': 'nurse','visit_cost': 500,'avatar': 'http://beauty-around.com/images/sampledata/Italian_Model/4Vanessa_Hessler_61.jpg', 'title': ['Узкий']},
        {'name': 'Lius','surname': 'Lein','position': 'neurologist','visit_cost': '10000','avatar': 'http://beauty-around.com/images/sampledata/Italian_Model/3bianca_balti.jpg', 'title': ['Узкий']},
    ]

    def handle(self, *args, **options):
        holding = ServiceProvidingHolding.objects.create(
            name='Aibolit'
        )

        for user in self.user_list:
            s_p = ServiceProvider(
                name=user['name'],
                surname=user['surname'],
                position=user['position'],
                service_providing_holding=holding,
                visit_cost=user['visit_cost'],
                avatar=user['avatar']
            )

            s_p.save()
            for tit in user['title']:
                category = Category.objects.filter(title__contains=tit).first()
                if category:
                    s_p.categories.add(category)
