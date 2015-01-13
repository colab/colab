"""
Test User class.
Objective: Test parameters, and behavior.
"""
from colab.accounts.models import User
from django.test import TestCase, Client


class UserTest(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()

    def tearDown(self):
        pass

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

    def test_check_password(self):
        self.assertTrue(self.user.check_password("123colab4"))
        self.assertFalse(self.user.check_password("1234"))

    def test_get_absolute_url(self):
        url = self.user.get_absolute_url()
        self.assertEqual("/account/usertestcolab", url)

    def test_twitter_link(self):
        link_twitter = self.user.twitter_link()
        self.assertEqual('https://twitter.com/usertestcolab', link_twitter)

    def test_facebook_link(self):
        link_facebook = self.user.facebook_link()
        self.assertEqual('https://www.facebook.com/usertestcolab',
                         link_facebook)

    def test_mailinglists(self):
        empty_list = ()
        self.assertEqual(empty_list, self.user.mailinglists())

    def test_update_subscription(self):
        pass
        # TODO: You should have mailman connection.

    def test_save(self):
        username_test = "USERtestCoLaB"

        user_db = User.objects.get(id=1)
        self.assertEqual(user_db.username, username_test.lower())
        self.user.delete()

    def test_update_user_mandatory_information(self):
        self.authenticate_user()

        data = {'first_name': 'usercolabtest',
                'last_name': 'colabtest'}
        self.client.post('/account/usertestcolab/edit', data)

        user = User.objects.get(id=1)

        self.assertEqual('usercolabtest', user.first_name)
        self.assertEqual('colabtest', user.last_name)
        self.user.delete()

    def test_update_user_mandatory_invalid_information(self):
        self.authenticate_user()

        data = {'first_name': 'a' * 31,
                'last_name': 'a' * 31}
        self.client.post('/account/usertestcolab/edit', data)

        user = User.objects.get(id=1)

        self.assertEqual('USERtestCoLaB', user.first_name)
        self.assertEqual('COLAB', user.last_name)

    def test_update_user_all_information(self):
        self.authenticate_user()

        data = {'first_name': 'Colab',
                'last_name': 'Test',
                'institution': 'fga',
                'role': 'tester',
                'twitter': 'twitter',
                'facebook': 'facebook',
                'google_talk': 'gtalk',
                'github': 'github',
                'webpage': 'webpage',
                'bio': 'bio'}
