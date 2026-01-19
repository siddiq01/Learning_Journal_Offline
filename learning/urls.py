from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import auth_views
from django.views.decorators.cache import never_cache

urlpatterns = [

    # --- ADD THESE FOR AUTH ---
    path('login/', never_cache(auth_views.LoginView.as_view()), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # --- PUBLIC PAGES ---
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),

    # --- SUBJECT & TOPIC HIERARCHY ---
    # subject/python/projects/
    path('subject/<slug:slug>/projects/', views.subject_projects, name='subject_projects'),
    
    # subject/python/
    path('subject/<slug:slug>/', views.subject_topics, name='subject_topics'),

    # subject/python/django-basics/
    path('subject/<slug:subject_slug>/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
    
    # projects/1/
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),


    # --- CONTRIBUTOR DASHBOARD & EDITOR ---
    path('dashboard/', views.contributor_dashboard, name='contributor_dashboard'),
    path('topic/new/', views.create_topic, name='topic_create'),
    path('topic/<int:pk>/edit/', views.edit_topic, name='topic_edit'),


    # --- PROFESSIONAL MODERATION SYSTEM ---
    # The main queue for real-time monitoring
    path('moderate/', views.moderation_queue, name='moderation_queue'),
    
    # Detailed review page for a specific topic
    path('moderate/review/<int:pk>/', views.moderation_review, name='moderation_review'),
    
    # Approval action (usually called via POST button in queue)
    path('moderate/approve/<int:pk>/', views.approve_topic, name='approve_topic'),


    # --- AUTHENTICATION ---
    path('signup/', views.signup, name='signup'),

    path('topic/<int:pk>/delete/', views.delete_topic, name='topic_delete'),

    path('moderate/reject/<int:pk>/', views.reject_topic, name='reject_topic'),
]