    from trac.core import *
    from trac.config import BoolOption
    from trac.web.api import IAuthenticator

    class MyRemoteUserAuthenticator(Component):

        implements(IAuthenticator)

        obey_remote_user_header = BoolOption('trac', 'obey_remote_user_header', 'false',
                   """Whether the 'Remote-User:' HTTP header is to be trusted for user logins 
                    (''since ??.??').""")

        def authenticate(self, req):
            if self.obey_remote_user_header and req.get_header('Remote-User'):
                return req.get_header('Remote-User')
            return None

