from django.shortcuts import redirect

class AdminRedirectMixin():
    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_staff or request.user.is_superuser) and not request.user.groups.filter(name='Преподаватели'):
            return redirect('admin/')
        return super().dispatch(request, *args, **kwargs)