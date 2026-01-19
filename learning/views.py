from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Added AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import Subject, Topic, Project 
from .forms import TopicForm 
from .decorators import role_required

# --- AUTH & PUBLIC VIEWS ---

@never_cache 
def login_view(request):
    """Handles login and prevents authenticated users from seeing the form via back button."""
    # 1. If already logged in, redirect immediately
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    # We define the context dictionary locally here
    context_data = {'form': form}
    return render(request, 'registration/login.html', context_data)

@never_cache  # Added to prevent caching the home state (logged in vs logged out)
def home(request):
    """Public landing page showing only live topics."""
    topics = Topic.objects.filter(status='published').order_by('-created_at')
    return render(request, 'home.html', {'topics': topics})

def subject_topics(request, slug):
    """List of published topics within a specific subject."""
    subject = get_object_or_404(Subject, slug=slug)
    nav_subjects = Subject.objects.filter(is_active=True)
    topics = Topic.objects.filter(subject=subject, status='published')
    return render(request, 'subject_topics.html', {
        'subject': subject,
        'topics': topics,
        'nav_subjects': nav_subjects,
    })

# ADDED TO FIX URL ERRORS
def subject_projects(request, slug):
    """subject/python/projects/"""
    subject = get_object_or_404(Subject, slug=slug)
    projects = Project.objects.filter(subject=subject)
    return render(request, 'learning/subject_projects.html', {'subject': subject, 'projects': projects})

def topic_detail(request, subject_slug, topic_slug):
    """Detailed article view."""
    topic = get_object_or_404(Topic, slug=topic_slug, subject__slug=subject_slug, status='published')
    sidebar_topics = Topic.objects.filter(subject=topic.subject, status='published').order_by('id')

    next_topic = Topic.objects.filter(
        subject=topic.subject, 
        status='published', 
        id__gt=topic.id
    ).order_by('id').first()

    previous_topic = Topic.objects.filter(
        subject=topic.subject, 
        status='published', 
        id__lt=topic.id
    ).order_by('-id').first()

    context = {
        'topic': topic,
        'sidebar_topics': sidebar_topics,
        'next_topic': next_topic,
        'previous_topic': previous_topic,
    }
    return render(request, 'learning/topic_detail.html', context)

# ADDED TO FIX URL ERRORS
def project_detail(request, pk):
    """projects/1/"""
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'learning/project_detail.html', {'project': project})

def search(request):
    """Search functionality restricted to published content."""
    query = request.GET.get('q', '').strip()
    
    if query:
        # We assign the queryset to a variable named 'results' 
        # to match your search_results.html template
        results = Topic.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).distinct()
    else:
        results = Topic.objects.none()

    return render(request, 'search_results.html', {
        'query': query, 
        'results': results  # This MUST match the {% for topic in results %} in your HTML
    })


# --- CONTRIBUTOR VIEWS (Security Applied) ---

@never_cache
@login_required
@role_required(allowed_roles=['contributor', 'moderator', 'admin'])
def contributor_dashboard(request):
    """Author's personal workspace."""
    user_topics = Topic.objects.filter(author=request.user).order_by('-updated_at')
    
    context = {
        'drafts': user_topics.filter(status='draft'),
        'rejected': user_topics.filter(status='rejected'),
        'pending': user_topics.filter(status='pending'),
        'approved': user_topics.filter(status='published'),
    }
    return render(request, 'learning/contributor_dashboard.html', context)

@never_cache
@login_required
@role_required(allowed_roles=['contributor', 'moderator', 'admin'])
def create_topic(request):
    """Submit a new topic."""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, "Topic created successfully!")
            return redirect('contributor_dashboard')
    else:
        form = TopicForm()
    return render(request, 'learning/topic_form.html', {'form': form, 'action': 'Create'})

@never_cache
@login_required
@role_required(allowed_roles=['contributor', 'moderator', 'admin'])
def edit_topic(request, pk):
    """Edit existing topic and handle resubmission logic."""
    topic = get_object_or_404(Topic, pk=pk)
    
    if topic.author != request.user and request.user.profile.role not in ['admin', 'moderator']:
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            updated_topic = form.save(commit=False)
            if updated_topic.status == 'rejected':
                updated_topic.status = 'pending'
            updated_topic.save()
            messages.success(request, "Topic updated and resubmitted for review!")
            return redirect('contributor_dashboard')
    else:
        form = TopicForm(instance=topic)
    return render(request, 'learning/topic_form.html', {'form': form, 'action': 'Edit'})


# --- MODERATION VIEWS (Restricted to Staff) ---

@never_cache
@login_required
@role_required(allowed_roles=['admin', 'moderator'])
def moderation_queue(request):
    """Central hub for moderators."""
    pending_topics = Topic.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'learning/moderation_queue.html', {'pending_topics': pending_topics})

@never_cache
@login_required
@role_required(allowed_roles=['admin', 'moderator'])
def moderation_review(request, pk):
    """Full detail review before publishing."""
    topic = get_object_or_404(Topic, pk=pk, status='pending')
    return render(request, 'learning/moderation_review.html', {'topic': topic})

@never_cache # Added to prevent caching review actions
@login_required
@role_required(allowed_roles=['admin', 'moderator'])
def approve_topic(request, pk):
    """Change status to published to make it live."""
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.status = 'published'
        topic.rejection_notes = "" 
        topic.save()
        messages.success(request, f"'{topic.title}' is now live on the platform!")
    return redirect('moderation_queue')

@never_cache # Added to prevent caching review actions
@login_required
@role_required(allowed_roles=['admin', 'moderator'])
def reject_topic(request, pk):
    """Send back to author with feedback."""
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        if not feedback:
            messages.error(request, "Please provide feedback before requesting changes.")
            return redirect('moderation_review', pk=pk)
            
        topic.status = 'rejected'
        topic.rejection_notes = feedback
        topic.save()
        messages.warning(request, f"Changes requested for '{topic.title}'.")
    return redirect('moderation_queue')


# --- AUTH & PROJECTS ---

@never_cache # Prevent accessing signup via back-button when logged in
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Account created! Welcome to the Contributor Portal.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@never_cache
@login_required
def delete_topic(request, pk):
    """Safe delete: users only delete their own content."""
    topic = get_object_or_404(Topic, pk=pk, author=request.user)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, "Topic deleted successfully.")
    return redirect('contributor_dashboard')