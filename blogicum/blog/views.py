from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import ModelFormMixin

from .forms import CommentForm, PostForm
from .mixins import (
    OnlyAuthorMixin,
    PostMixin,
    CommentMixin,
)
from .models import Post, Category, Comment
import blog.constants as cnsts


User = get_user_model()


def annotate_comment_count(posts):
    return posts.select_related(
        'author',
        'category',
        'location'
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def filtered_posts_by_publication(posts):
    return posts.filter(
        pub_date__date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


class PostsHomepageView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = cnsts.NUM_OF_POSTS
    queryset = filtered_posts_by_publication(
        annotate_comment_count(
            Post.objects.all()
        )
    ).order_by(*Post._meta.ordering)


class PostDetailView(ListView):
    model = Comment
    template_name = 'blog/detail.html'
    paginate_by = cnsts.NUM_OF_POSTS

    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post.author == self.request.user:
            return post
        return get_object_or_404(filtered_posts_by_publication(
            Post.objects),
            pk=self.kwargs['post_id']
        )

    def get_queryset(self):
        return self.get_post().comments.all().order_by(*Comment._meta.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_post()
        return context


class CategoryPostsView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = cnsts.NUM_OF_POSTS

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )

    def get_queryset(self):
        return filtered_posts_by_publication(
            annotate_comment_count(
                self.get_category().posts.all()
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    context_object_name = 'posts'
    paginate_by = cnsts.NUM_OF_POSTS

    def get_author(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        posts = annotate_comment_count(
            self.get_author().posts.all()
        )
        if self.get_author() != self.request.user:
            posts = filtered_posts_by_publication(posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_author()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, UpdateView):

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={self.pk_url_kwarg: self.object.id}
        )


class PostDeleteView(PostMixin, ModelFormMixin, DeleteView):
    pass


class CommentCreateView(CommentMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(CommentMixin, OnlyAuthorMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    pass
