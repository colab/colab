from django.conf import settings

def social_network_enabled(request):
    return {'SOCIAL_NETWORK_ENABLED': getattr(settings,
                                              'SOCIAL_NETWORK_ENABLED',
                                              False)}


def redirect_login(request):
    previous_path = request.COOKIES.get('_previous_path')
    print previous_path
    if previous_path is None:
        print "entrou no if"
        return {'previous_path': '/dashboard'}
    else:
        print "entrou no else"
        return {'previous_path': previous_path}
