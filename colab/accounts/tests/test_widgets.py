from django.test import TestCase
from colab.accounts.models import User
from django.test import Client


class WidgetAccountTest(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()

    def create_user(self):
        user = User()
        user.username = "usertest"
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
        templates = ['widgets/group_membership.html',
                     'widgets/group.html',
                     'widgets/latest_contributions.html',
                     'widgets/latest_posted.html',
                     'widgets/collaboration_chart.html',
                     'widgets/participation_chart.html',
                     ]
        for template in templates:
            url = "/account/" + self.user.username
            response = self.get_response_from_request(url)
            self.assertTemplateUsed(
                template_name=template, response=response)
