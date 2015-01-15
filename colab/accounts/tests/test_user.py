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

    def validate_mandatory_fields(self, expected_first_name, expected_last_name,
                                  first_name, last_name):
        
        data = {'first_name': first_name,
                'last_name': last_name}
        self.client.post('/account/usertestcolab/edit', data)
        user = User.objects.get(id=1)
        self.assertEqual(expected_first_name, user.first_name)
        self.assertEqual(expected_last_name, user.last_name)

    def validate_non_mandatory_fields(self, field_name, expected_value, value):
        data = {'first_name': 'usertestcolab',
                'last_name': 'colab',
                field_name: value}
        self.client.post('/account/usertestcolab/edit', data)
        user = User.objects.get(id=1)
        self.assertEqual(expected_value, getattr(user, field_name))

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
        self.validate_mandatory_fields('usertestcolab', 'colabtest',
                                       'usertestcolab', 'colabtest')
        self.user.delete()

    def test_update_user_mandatory_max_leght_limit(self):
        self.authenticate_user()
        self.validate_mandatory_fields('a'*30, 'a'*30, 'a'*30, 'a'*30)
        self.user.delete()

    def test_update_user_mandatory_max_leght_limit_one_less(self):
        self.authenticate_user()
        self.validate_mandatory_fields('a'*29, 'a'*29, 'a'*29, 'a'*29)
        self.user.delete()

    def test_update_user_mandatory_max_leght_overflow(self):
        self.authenticate_user()                    
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB', 'a'*31, 'a'*31)
        self.user.delete()

    def test_update_user_mandatory_invalid_empty_field(self):
        self.authenticate_user()                    
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB', '' , '')
        self.user.delete()

    def test_update_user_mandatory_invalid_whitespace(self):
        self.authenticate_user()                    
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB', ' ' , ' ')
        self.user.delete()

    def test_update_user_mandatory_invalid_using_number(self):
        self.authenticate_user()                    
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB', '123' , '456')
        self.user.delete()

    def test_update_user_institution(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', 'fga', 'fga')
        self.user.delete()

    def test_update_user_role(self):
        self.authenticate_user()
        self.user.delete()
    
    def test_update_user_twitter(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', 'twitter', 'twitter')
        self.user.delete()
    
    def test_update_user_facebook(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', 'facebook', 'facebook')
        self.user.delete()
    
    def test_update_user_gtalk(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', 'gtalk@colab.com.br',
                                           'gtalk@colab.com.br')
        self.user.delete()
    
    def test_update_user_github(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', 'github', 'github')
        self.user.delete()
    
    def test_update_user_webpage(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', 'webpage', 'webpage')
        self.user.delete()

    def test_update_user_bio(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', 'bio', 'bio')
        self.user.delete()
        
    def test_update_user_bio_max_length(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', None, 'a' * 201)
        self.user.delete()
