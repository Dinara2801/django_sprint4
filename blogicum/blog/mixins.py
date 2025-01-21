from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import CommentForm, PostForm
from .models import Post, Comment


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        return redirect(
            reverse_lazy('blog:post_detail', args=[self.get_object().id])
        )


class PostMixin(OnlyAuthorMixin, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect(
            reverse_lazy('blog:post_detail', args=[self.get_object().id])
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
