from django.shortcuts import render

class HitCountViewMixin(object):
    def get_object(self):
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        response = super(HitCountViewMixin, self).dispatch(request,
                                                           *args, **kwargs)
        if 200 <= response.status_code < 300:
            obj = self.get_object()
            if obj: obj.hit(request)
        return response
