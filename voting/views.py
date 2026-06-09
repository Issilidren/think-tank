import logging
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Handle, Idea, Theme, Vote, Comment, CommentVote
from .forms import HandleForm, IdeaForm, ThemeForm, CommentForm

logger = logging.getLogger(__name__)


def user_profile(request, handle_id):
    handle = get_object_or_404(Handle, pk=handle_id)
    ideas = Idea.objects.filter(handle=handle).select_related('project').order_by('-submitted_at')
    votes = Vote.objects.filter(handle=handle).select_related('theme', 'theme__project').order_by('theme__project__title', 'theme__title')
    return render(request, 'voting/user_profile.html', {
        'profile_handle': handle,
        'ideas': ideas,
        'votes': votes,
    })


def project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    current_handle = None
    handle_id = request.session.get('handle_id')
    if handle_id:
        try:
            current_handle = Handle.objects.get(pk=handle_id)
        except Handle.DoesNotExist:
            del request.session['handle_id']

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'set_handle':
            form = HandleForm(request.POST)
            if form.is_valid():
                handle, _ = Handle.objects.get_or_create(name=form.cleaned_data['name'])
                handle.team = form.cleaned_data['team']
                handle.save()
                request.session['handle_id'] = handle.pk
            return redirect('voting:project', project_id=project_id)

        if action == 'submit_idea' and current_handle:
            if project.can_add_idea(current_handle):
                form = IdeaForm(request.POST)
                if form.is_valid():
                    idea = form.save(commit=False)
                    idea.project = project
                    idea.handle = current_handle
                    idea.save()
            return redirect('voting:project', project_id=project_id)

        if action == 'suggest_theme' and current_handle:
            form = ThemeForm(request.POST)
            if form.is_valid():
                theme = form.save(commit=False)
                theme.project = project
                theme.suggested_by = current_handle
                theme.save()
            return redirect('voting:project', project_id=project_id)

        if action == 'vote' and current_handle:
            theme_id = request.POST.get('theme_id')
            if theme_id:
                theme = get_object_or_404(Theme, pk=theme_id, project=project)
                vote, created = Vote.objects.get_or_create(theme=theme, handle=current_handle)
                if not created:
                    vote.delete()  # toggle: voting again takes the vote back
            return redirect('voting:project', project_id=project_id)

        if action == 'vote_comment' and current_handle:
            comment_id = request.POST.get('comment_id')
            if comment_id:
                comment = get_object_or_404(Comment, pk=comment_id, theme__project=project)
                cvote, created = CommentVote.objects.get_or_create(comment=comment, handle=current_handle)
                if not created:
                    cvote.delete()
            return redirect('voting:project', project_id=project_id)

        if action == 'comment' and current_handle:
            theme_id = request.POST.get('theme_id')
            form = CommentForm(request.POST)
            if theme_id and form.is_valid():
                theme = get_object_or_404(Theme, pk=theme_id, project=project)
                comment = form.save(commit=False)
                comment.theme = theme
                comment.handle = current_handle
                comment.save()
            return redirect('voting:project', project_id=project_id)

        # Deletes are owner-only: the filter on handle/suggested_by means you
        # can only ever remove your own posts, never a teammate's.
        if action == 'delete_idea' and current_handle:
            Idea.objects.filter(
                pk=request.POST.get('idea_id'), project=project, handle=current_handle,
            ).delete()
            return redirect('voting:project', project_id=project_id)

        if action == 'delete_theme' and current_handle:
            Theme.objects.filter(
                pk=request.POST.get('theme_id'), project=project, suggested_by=current_handle,
            ).delete()
            return redirect('voting:project', project_id=project_id)

        if action == 'delete_comment' and current_handle:
            Comment.objects.filter(
                pk=request.POST.get('comment_id'), theme__project=project, handle=current_handle,
            ).delete()
            return redirect('voting:project', project_id=project_id)

        return redirect('voting:project', project_id=project_id)

    ideas = project.ideas.select_related('handle').all()
    themes = list(
        project.themes.select_related('suggested_by')
        .prefetch_related('votes', 'comments__handle', 'comments__votes')
        .order_by('-created_at')
    )

    # % tally: each theme's share of all votes cast in this poll.
    total_votes = sum(t.vote_count for t in themes)
    leader_id = None
    best = 0
    for t in themes:
        t.vote_pct = round(100 * t.vote_count / total_votes) if total_votes else 0
        if t.vote_count > best:
            best, leader_id = t.vote_count, t.pk
        # mark the top-voted "build" in each thread
        t.top_comment_id = None
        top = 0
        for c in t.comments.all():
            if c.vote_count > top:
                top, t.top_comment_id = c.vote_count, c.pk

    voted_theme_ids = set()
    voted_comment_ids = set()
    if current_handle:
        voted_theme_ids = set(
            Vote.objects.filter(handle=current_handle, theme__project=project)
            .values_list('theme_id', flat=True)
        )
        voted_comment_ids = set(
            CommentVote.objects.filter(handle=current_handle, comment__theme__project=project)
            .values_list('comment_id', flat=True)
        )

    return render(request, 'voting/project.html', {
        'project': project,
        'current_handle': current_handle,
        'handle_form': HandleForm(),
        'idea_form': IdeaForm(),
        'theme_form': ThemeForm(),
        'ideas': ideas,
        'themes': themes,
        'voted_theme_ids': voted_theme_ids,
        'voted_comment_ids': voted_comment_ids,
        'leader_id': leader_id,
        'total_votes': total_votes,
    })
