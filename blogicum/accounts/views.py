from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse


User = get_user_model()


class RegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username}
        )
