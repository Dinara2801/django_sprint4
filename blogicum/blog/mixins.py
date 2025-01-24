from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Post, Comment


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user == self.get_object().author


class PostMixin(OnlyAuthorMixin, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        post_id = self.kwargs[self.pk_url_kwarg]
        return redirect(
            reverse(
                'blog:post_detail',
                kwargs={self.pk_url_kwarg: post_id}
            )
        )

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = self.form_class(instance=post)
        return context


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
