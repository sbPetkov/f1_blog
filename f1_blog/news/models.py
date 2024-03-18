from django.db import models
from django.contrib.auth.models import User


def upload_to_news_photos(instance, filename):
    return 'news_photos/{0}/{1}'.format(instance.author.username, filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to=upload_to_news_photos, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_post_comments', blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def liked_by_current_user(self, user):
        return user in self.likes.all()
