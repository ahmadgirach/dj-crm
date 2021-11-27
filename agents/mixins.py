from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganiserAndLoginRequiredMixin(AccessMixin):
    """ Verify that the current user is authenticated or an organiser. """
    def dispatch(self, request, *args, **kwargs):
        current_user = request.user

        if not (current_user.is_authenticated or current_user.is_organiser):
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
