from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)


from .forms import CommentForm, PostForm
from .mixins import (
    CommentGetObjectMixin,
    OnlyAuthorMixin,
    PostQuerySetMixin,
    PostSuccessUrlMixin,
    ProfileSuccessUrlMixin
)
from .models import Post, Category, Comment
import blog.constants as cnsts


User = get_user_model()


class PostsHomepageView(PostQuerySetMixin, ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True).order_by(
            '-pub_date'
        ).select_related('author', 'category', 'location')
    paginate_by = cnsts.NUM_OF_POSTS


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.author == self.request.user:
            return post
        else:
            return get_object_or_404(
                Post,
                pk=self.kwargs['pk'],
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CategoryPostsView(PostQuerySetMixin, ListView):
    template_name = 'blog/category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug']
        )
        if not category.is_published:
            raise Http404("Категория не найдена или снята с публикации.")
        return super().get_queryset().filter(
            category=category
        ).order_by('-pub_date').select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['posts']:
            context['category'] = context['posts'][0].category
        else:
            context['category'] = None
        return context

    paginate_by = cnsts.NUM_OF_POSTS


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            author__username=self.kwargs['username'],
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date').select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['posts']:
            context['profile'] = context['posts'][0].author
        else:
            context['profile'] = get_object_or_404(
                User,
                username=self.kwargs['username']
            )
        context['username'] = context['profile'].username
        return context

    paginate_by = cnsts.NUM_OF_POSTS


class ProfileUpdateView(
    ProfileSuccessUrlMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    UpdateView
):
    form_class = UserChangeForm
    template_name = 'blog/user.html'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def test_func(self):
        return self.request.user == self.get_object()


class PostCreateView(
    ProfileSuccessUrlMixin,
    LoginRequiredMixin,
    CreateView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    PostSuccessUrlMixin,
    OnlyAuthorMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = {'instance': self.object}
        return context


class CommentCreateView(
    PostSuccessUrlMixin,
    LoginRequiredMixin,
    CreateView
):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.current_post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.current_post
        return super().form_valid(form)


class CommentUpdateView(
    CommentGetObjectMixin,
    OnlyAuthorMixin,
    PostSuccessUrlMixin,
    UpdateView
):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'


class CommentDeleteView(
    CommentGetObjectMixin,
    OnlyAuthorMixin,
    PostSuccessUrlMixin,
    DeleteView
):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
