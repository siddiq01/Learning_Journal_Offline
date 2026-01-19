from .models import Subject

def subjects_processor(request):
    # 🟢 Show all active subjects so the sidebar is populated immediately
    nav_subjects = Subject.objects.filter(is_active=True).order_by('display_order')

    return {
        'nav_subjects': nav_subjects
    }