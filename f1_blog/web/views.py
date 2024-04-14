from datetime import date

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, View, CreateView, UpdateView
from django.utils.http import url_has_allowed_host_and_scheme

from f1_blog.merchandise.models import Category
from f1_blog.news.models import Post
from f1_blog.standings.models import Race
from f1_blog.videos.models import Video
from f1_blog.web.forms import FOneUserCreationForm
from f1_blog.web.models import Profile


def index(request):
    today = date.today()
    next_race = Race.objects.filter(start_date__gt=today).order_by('start_date').first()
    last_news = Post.objects.all().order_by('-created_at')[:2]
    last_videos = Video.objects.all().order_by('-created_at')[:2]
    merchandise = Category.objects.all()
    context = {
        'next_race': next_race,
        'last_news': last_news,
        'merchandise': merchandise,
        'last_videos': last_videos
    }

    return render(request, 'index/index.html', context)


class SearchResultsView(ListView):
    template_name = 'index/search_results.html'
    context_object_name = 'context'

    def get_queryset(self):
        query = self.request.GET.get('query')
        news_results = Post.objects.filter(title__icontains=query)
        video_results = Video.objects.filter(title__icontains=query)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        news_results = Post.objects.filter(title__icontains=query)
        video_results = Video.objects.filter(title__icontains=query)

        context['news_results'] = news_results
        context['video_results'] = video_results
        context['query'] = query
        return context


class LoginUserView(LoginView):
    template_name = 'index/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_to = self.request.GET.get('next')
        if redirect_to and url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={self.request.get_host()}):
            return redirect_to
        return super().get_success_url()


class RegisterUserView(CreateView):
    template_name = 'index/register.html'
    form_class = FOneUserCreationForm

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, form.instance)
        return result


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'index/profile.html'
    model = Profile


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'address', 'phone_number']
    template_name = 'index/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class IsModeratorOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists() or self.request.user.is_staff


class AdministrationView(LoginRequiredMixin, IsModeratorOrAdminMixin, TemplateView):
    template_name = 'administration.html'
