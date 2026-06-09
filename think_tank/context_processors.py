from django.conf import settings


def github_repo(request):
    return {'GITHUB_REPO_URL': getattr(settings, 'GITHUB_REPO_URL', '')}
