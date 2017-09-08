from django.shortcuts import redirect


class LoginMixin(object):

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect('/')
        return super().dispatch(*args, **kwargs)
