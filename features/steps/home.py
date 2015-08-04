

@when(u'I access the URL "{url}"')
def step_impl(context, url):
    context.response = context.test.client.get(url)

@then(u'The browser URL should be "{url}"')
def step_impl(context, url):
    context.test.assertRedirects(context.response, url, status_code=301)
