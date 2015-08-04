
from colab.celery import app


@app.task(bind=True)
def handling_method(self, **kwargs):
    f = open('/vagrant/test_plugin', 'wb')
    f.write(str(kwargs))
    f.close()
    return 5
