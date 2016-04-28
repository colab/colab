from colab.accounts.models import User
from behave import given, when


@given(u'The user "{username}" with the password "{password}" is "{status}"')
def create_user(context, username, password, status):
    user = User()
    user.username = username
    user.set_password(password)
    user.email = "usertest@colab.com.br"
    user.id = 1
    user.first_name = "USERtestCoLaB"
    user.last_name = "COLAB"
    user.needs_update = False
    if status == "active":
        user.is_active = True
    else:
        user.is_active = False
    user.save()


@given(u'I am logged in as "{username}"')
def step_impl(context, username):
    context.execute_steps('''
        When I access the URL "/"
        When I click in "Acesso "
        When I click in "Login"
        Given The user "%s" with the password "%s" is "%s"
        When I fill "%s" in "id_username" field
        When I fill "%s" in "id_password" field
        When I click in "Login" button
    ''' % (username, username, 'active', username, username))


@when(u'I open the user menu')
def step_impl(context):
    dropdown = context.driver.find_element_by_id('user-menu')
    dropdown.find_element_by_xpath('.//a').click()
