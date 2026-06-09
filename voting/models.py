from django.db import models

TEAM_CHOICES = [
    ('404', '404 Brain not found!'),
    ('da_koders', 'Da_Koders'),
]


class Handle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'@{self.name}'

    @property
    def team_label(self):
        return dict(TEAM_CHOICES).get(self.team, 'Unknown')


class Project(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Idea(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ideas')
    handle = models.ForeignKey(Handle, on_delete=models.CASCADE, related_name='ideas')
    text = models.CharField(max_length=300)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.handle.name}: {self.text[:50]}'


class Theme(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='themes')
    title = models.CharField(max_length=100)
    suggested_by = models.ForeignKey(Handle, on_delete=models.CASCADE, related_name='suggested_themes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def vote_count(self):
        return self.votes.count()


class Vote(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='votes')
    handle = models.ForeignKey(Handle, on_delete=models.CASCADE, related_name='votes')

    class Meta:
        unique_together = ('theme', 'handle')
