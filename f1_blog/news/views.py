from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
        # Fetch the last post
        last_post = Post.objects.order_by('-created_at').first()
        context['last_post'] = last_post
        # Fetch the next two posts
        next_two_posts = Post.objects.exclude(id=last_post.id).order_by('-created_at')[:3]
        context['next_two_posts'] = next_two_posts
        # Fetch all other posts
        other_posts = Post.objects.exclude(id__in=[last_post.id] + [post.id for post in next_two_posts])
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
