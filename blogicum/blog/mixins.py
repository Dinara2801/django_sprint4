from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone


from .models import Post, Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        post = self.get_object()
        return redirect(reverse_lazy('blog:post_detail', args=[post.id]))


class PostQuerySetMixin:
    def get_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(comment_count=Count('comments'))


class ProfileSuccessUrlMixin:
    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostSuccessUrlMixin:
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']})


class CommentGetObjectMixin:
    def get_object(self):
        return get_object_or_404(
            Comment,
            pk=self.kwargs['id'], post_id=self.kwargs['pk'])
