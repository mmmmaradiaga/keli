from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar        = models.ImageField(upload_to='avatars/', null=True, blank=True)
    avatar_color  = models.CharField(max_length=60, default='135deg,#6b6358,#a09484')
    is_verified   = models.BooleanField(default=False)

    @property
    def initials(self):
        parts = self.user.get_full_name().split()
        return ''.join(p[0].upper() for p in parts[:2]) if parts else self.user.username[:2].upper()

    def __str__(self):
        return f'Profile({self.user.username})'


class Post(models.Model):
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body        = models.TextField(max_length=280, null=False, blank=False)
    attachment  = models.ImageField(upload_to='posts/', null=True, blank=True)
    quote       = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='quoted_by')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post({self.author.username}, {self.created_at:%Y-%m-%d})'
    # # M2M for likes and reposts — clean, queryable, no count denormalization needed at small scale
    # likes       = models.ManyToManyField(User, related_name='liked_posts',    blank=True)
    # reposts     = models.ManyToManyField(User, related_name='reposted_posts', blank=True)

    # class Meta:
    #     ordering = ['-created_at']

    # @property
    # def likes_count(self):
    #     return self.likes.count()

    # @property
    # def reposts_count(self):
    #     return self.reposts.count()

    # @property
    # def comments_count(self):
    #     # assumes Comment model with FK to Post
    #     return self.comments.count()


