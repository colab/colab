from selenium import webdriver


def before_feature(context, feature):
    context.driver = webdriver.Firefox()
    context.driver.set_window_size(1000, 600)
    context.driver.implicitly_wait(5)


def after_feature(context, feature):
    context.driver.quit()
