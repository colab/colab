"""
Test User class.
Objective: Test parameters, and behavior.
"""
import mock

from colab.accounts.models import User
from colab.accounts import forms as accounts_forms
from django.test import TestCase, Client


class UserTest(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()
        accounts_forms.validate_social_account = mock.Mock(return_value=True)

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

    def validate_mandatory_fields(self, expected_first_name,
                                  expected_last_name, first_name, last_name):
        data = {'first_name': first_name,
                'last_name': last_name,
                'colab_form': 'true'}
        self.client.post('/account/' + self.user.username + '/edit', data)
        user = User.objects.get(id=1)
        self.assertEqual(expected_first_name, user.first_name)
        self.assertEqual(expected_last_name, user.last_name)

    def validate_non_mandatory_fields(self, field_name, expected_value, value):
        data = {'first_name': 'usertestcolab',
                'last_name': 'colab',
                field_name: value,
                'colab_form': 'true'}
        self.client.post('/account/' + self.user.username + '/edit', data)
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
        self.validate_mandatory_fields('a' * 30, 'a' * 30, 'a' * 30, 'a' * 30)
        self.user.delete()

    def test_update_user_mandatory_max_leght_limit_one_less(self):
        self.authenticate_user()
        self.validate_mandatory_fields('a' * 29, 'a' * 29, 'a' * 29, 'a' * 29)
        self.user.delete()

    def test_update_user_mandatory_max_leght_overflow(self):
        self.authenticate_user()
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB',
                                       'a'*31, 'a'*31)
        self.user.delete()

    def test_update_user_mandatory_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB', '', '')
        self.user.delete()

    def test_update_user_mandatory_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_mandatory_fields('USERtestCoLaB', 'COLAB', ' ', ' ')
        self.user.delete()

    def test_update_user_institution(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', 'fga', 'fga')
        self.user.delete()

    def test_update_user_institution_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', 'a' * 128, 'a' * 128)
        self.user.delete()

    def test_update_user_institution_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', 'a' * 127, 'a' * 127)
        self.user.delete()

    def test_update_user_institution_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', None, 'a' * 129)
        self.user.delete()

    def test_update_user_institution_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', '', '')
        self.user.delete()

    def test_update_user_institution_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('institution', '', ' ')
        self.user.delete()

    def test_update_user_role(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('role', 'studenty', 'studenty')
        self.user.delete()

    def test_update_user_role_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('role', 'a' * 128, 'a' * 128)
        self.user.delete()

    def test_update_user_role_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('role', 'a' * 127, 'a' * 127)
        self.user.delete()

    def test_update_user_role_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('role', None, 'a' * 129)
        self.user.delete()

    def test_update_user_role_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('role', '', '')
        self.user.delete()

    def test_update_user_role_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('role', '', ' ')
        self.user.delete()

    def test_update_user_twitter(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', 'twitter', 'twitter')
        self.user.delete()

    '''
    Max_lenght is the maximmum size accept by Twitter.
    Tests related with twitter should have internet connection,
    because it's need username authentication.
    '''
    def test_update_user_twitter_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', 't' * 15, 't' * 15)
        self.user.delete()

    def test_update_user_twitter_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', 't' * 14, 't' * 14)
        self.user.delete()

    def test_update_user_twitter_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', 'usertestcolab',
                                           't' * 16)
        self.user.delete()

    def test_update_user_twitter_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', '', '')
        self.user.delete()

    def test_update_user_twitter_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('twitter', 'usertestcolab', ' ')
        self.user.delete()

    '''
    Max_lenght is the maximmum size accept by Faceebook.
    Tests related with twitter should have internet connection,
    because it's need username authentication.
    '''
    def test_update_user_facebook(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', 'facebook', 'facebook')
        self.user.delete()

    def test_update_user_facebook_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', 'f' * 15, 'f' * 15)
        self.user.delete()

    def test_update_user_facebook_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', 'f' * 14, 'f' * 14)
        self.user.delete()

    def test_update_user_facebook_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', 'usertestcolab',
                                           'f' * 16)
        self.user.delete()

    def test_update_user_facebook_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', '', '')
        self.user.delete()

    def test_update_user_facebook_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('facebook', 'usertestcolab', ' ')
        self.user.delete()

    def test_update_user_gtalk(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', 'gtalk@colab.com.br',
                                           'gtalk@colab.com.br')
        self.user.delete()

    def test_update_user_gtalk_email_invalid_caracters(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', None, '@@@')
        self.user.delete()

    def test_update_user_gtalk_email_without_arroba(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', None,
                                           'usercolab.hotmail.com')
        self.user.delete()

    def test_update_user_gtalk_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', None,
                                           'usercolab@hotmail')
        self.user.delete()

    def test_update_user_gtalk_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', '', '')
        self.user.delete()

    def test_update_user_gtalk_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('google_talk', '', ' ')
        self.user.delete()

    def test_update_user_github(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', 'github', 'github')
        self.user.delete()

    def test_update_user_github_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', 'a' * 39, 'a' * 39)
        self.user.delete()

    def test_update_user_github_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', 'a' * 38, 'a' * 38)
        self.user.delete()

    def test_update_user_github_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', None, 'a' * 40)
        self.user.delete()

    def test_update_user_github_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', '', '')
        self.user.delete()

    def test_update_user_github_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('github', '', ' ')
        self.user.delete()

    def test_update_user_webpage(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', 'webpage', 'webpage')
        self.user.delete()

    def test_update_user_webpage_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', 'p' * 256, 'p' * 256)
        self.user.delete()

    def test_update_user_webpage_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', 'p' * 255, 'p' * 255)
        self.user.delete()

    def test_update_user_webpage_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', None, 'p' * 257)
        self.user.delete()

    def test_update_user_webpage_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', '', '')
        self.user.delete()

    def test_update_user_webpage_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('webpage', '', ' ')
        self.user.delete()

    def test_update_user_bio(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', 'bio', 'bio')
        self.user.delete()

    def test_update_user_bio_max_lenght_limit(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', 'a' * 200, 'a' * 200)
        self.user.delete()

    def test_update_user_bio_max_lenght_limit_one_less(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', 'a' * 199, 'a' * 199)
        self.user.delete()

    def test_update_user_bio_max_lenght_overflow(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', None, 'a' * 201)
        self.user.delete()

    def test_update_user_bio_invalid_empty_field(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', '', '')
        self.user.delete()

    def test_update_user_bio_invalid_whitespace(self):
        self.authenticate_user()
        self.validate_non_mandatory_fields('bio', '', ' ')
        self.user.delete()

    def test_user_without_login(self):
        response = self.client.get("/account/" + self.user.username + "/edit")
        self.assertEqual(response.status_code, 403)

    def test_signup_with_post_not_success(self):
        data_user = {
            'username': 'username',
            'password1': 'safepassword',
            'password2': 'safepassword',
        }
        before = User.objects.count()
        self.client.post('/account/register', data=data_user)
        after = User.objects.count()
        self.assertEqual(before, after)

    def test_signup_with_post_with_success(self):
        data_user = {
            'username': 'username',
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'mail@mail.com',
            'password1': 'safepassword',
            'password2': 'safepassword',
        }
        before = User.objects.count()
        self.client.post('/account/register', data=data_user)
        after = User.objects.count()
        self.assertEqual(before + 1, after)

    def test_user_logged_in_profile(self):
        self.authenticate_user()
        self.client.get("/account/" + self.user.username)
        self.assertEqual(self.client.session['_auth_user_id'], self.user.id)

    def test_user_not_logged_in_profile(self):
        self.client.get("/account/" + self.user.username)
        self.assertEqual(self.client.session, {})

    def test_password_changed_message(self):
        self.message_test('Your password was changed.',
                          "/account/change-password-done")

    def test_password_reset_done_custom_message(self):
        self.message_test("We&#39;ve emailed you instructions for setting " +
                          "your password. You should be receiving them " +
                          "shortly.", "/account/password-reset-done/")

    def test_password_rest_complete_message(self):
        self.message_test("Your password has been set. You may go ahead and " +
                          "log in now.", "/account/password-reset-complete/")

    def message_test(self, message, url):
        self.authenticate_user()
        response = self.client.get(url, follow=True)
        self.assertIn(message, response.content)

    @mock.patch('colab.accounts.signals.user_password_changed.send')
    @mock.patch('colab.accounts.signals.user_created.send')
    def test_user_created_signal(self, user_created_send,
                                 user_password_changed_send):
        user = User.objects.create_user(
            username='test_user',
            password='12345',
            email='test@example.com',
        )
        user_created_send.assert_called_with(User, user=user, password='12345')
        user_password_changed_send.assert_not_called()

    @mock.patch('colab.accounts.signals.user_password_changed.send')
    def test_user_password_changed_signal(self, user_password_changed_send):
        user = User.objects.first()
        user.set_password('54321')
        user_password_changed_send.assert_called_with(User, user=user,
                                                      password='54321')
