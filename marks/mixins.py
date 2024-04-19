from django.shortcuts import redirect

class AdminRedirectMixin():
    def dispatch(self, request, *args, **kwargs):
        if (request.user.groups.filter(name='Администрация') and request.user.groups.count == 1) or request.user.is_superuser:
            return redirect('admin/')
        return super().dispatch(request, *args, **kwargs)