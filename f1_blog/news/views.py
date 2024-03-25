from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from f1_blog.news.models import Post, PostComment


class PostListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('post_comments')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_post = Post.objects.order_by('-created_at').first()
        context['last_post'] = last_post

        next_two_posts = Post.objects.exclude(id=last_post.id).order_by('-created_at')[:3]
        context['next_two_posts'] = next_two_posts

        other_posts = Post.objects.exclude(id__in=[last_post.id] + [post.id for post in next_two_posts]).order_by('-created_at')
        context['other_posts'] = other_posts

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.post_comments.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        text = request.POST.get('text')
        post = get_object_or_404(Post, pk=post_id)
        author = request.user
        comment = PostComment.objects.create(post=post, author=author, text=text)
        data = {
            'author_first_name': author.profile.first_name,
            'text': comment.text
        }
        return JsonResponse(data)


def toggle_comment_like(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_id)
        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': comment.likes.count()})


class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/add_news.html'
    fields = ['title', 'content', 'photo']
    permission_required = 'post.add_post'
    login_url = '/accounts/login/'
    success_url = reverse_lazy('post-index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
