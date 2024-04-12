from django.http import JsonResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Video, Comment


class AddVideoView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Video
    template_name = 'videos/add_video.html'
    fields = ['title', 'content', 'video']
    permission_required = 'videos.add_video'
    login_url = '/accounts/login/'
    success_url = reverse_lazy('video-index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('comments')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for video in context['videos']:
            video.last_comments = video.comments.order_by('-created_at')[:2]
        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()
        context['comments'] = video.comments.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        video_id = kwargs.get('pk')
        text = request.POST.get('text')
        video = Video.objects.get(pk=video_id)
        author = request.user
        author_name = request.user.profile.first_name
        comment = Comment.objects.create(video=video, author=author, text=text)
        data = {
            'author_name': author_name,
            'text': comment.text
        }
        return JsonResponse(data)


class VideoEditView(LoginRequiredMixin, UpdateView):
    model = Video
    template_name = 'videos/edit_video.html'
    fields = ['title', 'content', 'video']
    success_url = reverse_lazy('video-index')


class VideoDeleteView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'  # Your template name
    success_url = reverse_lazy('video-index')
