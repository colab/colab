
from django.test import TestCase
from colab.accounts.models import User
from django.test import Client


class WidgetAccountTest(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()

    def create_user(self):
        user = User()
        user.username = "USERtestCoLaB"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.twitter = "usertestcolab"
        user.facebook = "usertestcolab"
        user.first_name = "USERtestCoLaB"
        user.last_name = "COLAB"
        user.save()
        return user

    def authenticate_user(self):
        self.user.needs_update = False
        self.user.save()
        self.client.login(username=self.user.username,
                          password='123colab4')

    def get_response_from_request(self, addr):
        self.user = self.create_user()
        self.authenticate_user()
        response = self.client.get(addr)
        return response

    def test_account_widgets(self):
        templates = ['widgets/dashboard_collaboration_graph.html',
                     'widgets/dashboard_latest_collaborations.html',
                     'widgets/dashboard_most_relevant_threads.html',
                     ]
        for template in templates:
            response = self.get_response_from_request(
                "/dashboard")
            self.assertTemplateUsed(
                template_name=template, response=response)
