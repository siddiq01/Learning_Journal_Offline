from django.contrib import admin
from .models import Profile, Subject, Topic, Project, Category

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "trust_score")
    list_filter = ("role",)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "is_active")
    prepopulated_fields = {"slug": ("name",)}

# =====================================================
# TOPIC ADMIN (WITH AUTO-SLUG)
# =====================================================
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    # Added 'slug' and 'difficulty' to display
    list_display = ("title", "subject", "author", "status", "difficulty", "created_at")
    list_filter = ("subject", "status", "difficulty")
    search_fields = ("title", "content")
    
    # This makes the slug fill in automatically as you type the title
    prepopulated_fields = {"slug": ("title",)}
    
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "subject", "author", "status", "difficulty")
        }),
        ("Content Body", {
            "fields": ("content",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at"),
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "subject", "status", "created_at")