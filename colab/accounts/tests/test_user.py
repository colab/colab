"""
Test User class.
Objective: Test parameters, and behavior.
"""
from colab.accounts.models import User
from django.test import TestCase, Client

class UserTest(TestCase):
  
  def setUp(self):
    self.user = User()
    pass

  def test_check_password(self):
    pass

  def test_get_absolute_url(self):
    pass

  def test_twitter_link(self):
    pass
  
  def test_facebook_link(self):
    pass

  def test_mailinglist(self):
    pass

  def test_update_subscription(self):
    pass

  def test_save(self):
    username_test = "USERtestCoLaB"
    self.user.username = username_test
    self.user.set_password("123colab4")
    self.user.email = "usertest@colab.com.br"
    self.user.id = 1
    self.user.save()

    user_db = User.objects.get(id=1)
    self.assertEqual(user_db.username, username_test.lower())
    self.user.delete()
    

