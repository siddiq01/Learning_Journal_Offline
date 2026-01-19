from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

# Import learning app views
from learning import views as learning_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'favicon.ico',
        RedirectView.as_view(
            url=staticfiles_storage.url('images/favicon.ico'),
            permanent=True
        ),
    ),

    # 🟢 FIX: Map 'login/' to your custom protected view BEFORE the auth include
    path('login/', learning_views.login_view, name='login'),

    # Authentication (Remaining urls like password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # User Signup (Already protected in your views.py)
    path('signup/', learning_views.signup, name='signup'),

    # Learning App URLs
    path('', include('learning.urls')),

    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )