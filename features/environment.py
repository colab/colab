from selenium import webdriver
from django.conf import settings


def before_all(context):
  # Otherwise the ManifestStaticFilesStorage will use hashed names
  settings.DEBUG = True

def before_feature(context, feature):
    if 'selenium' in feature.tags:
        context.driver = webdriver.Firefox()
        context.driver.set_window_size(1000, 600)
        context.driver.implicitly_wait(5)
    else:
        context.driver = webdriver.PhantomJS()


def after_feature(context, feature):
    context.driver.quit()
