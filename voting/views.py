import logging
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Handle, Idea, Theme, Vote
from .forms import HandleForm, IdeaForm, ThemeForm

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
                Vote.objects.get_or_create(theme=theme, handle=current_handle)
            return redirect('voting:project', project_id=project_id)

        return redirect('voting:project', project_id=project_id)

    ideas = project.ideas.select_related('handle').all()
    themes = project.themes.select_related('suggested_by').prefetch_related('votes').order_by('-created_at')

    voted_theme_ids = set()
    if current_handle:
        voted_theme_ids = set(
            Vote.objects.filter(handle=current_handle, theme__project=project)
            .values_list('theme_id', flat=True)
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
    })
