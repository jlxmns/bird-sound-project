from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Bird, User, IdentificationReport, IdentificationResult


@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = (
        "common_name",
        "scientific_name",
        "family",
        "order",
        "conservation_status",
    )
    list_filter = ("family", "order", "conservation_status")
    search_fields = ("common_name", "scientific_name", "family")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("common_name",)

    fieldsets = (
        (
            "Identification",
            {"fields": ("common_name", "scientific_name", "order", "family")},
        ),
        ("Physical Traits", {"fields": ("wingspan", "weight", "length")}),
        ("Ecology", {"fields": ("habitat", "conservation_status")}),
        ("Media", {"fields": ("image", "description")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")

    fieldsets = BaseUserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (("Role", {"fields": ("role",)}),)


class IdentificationResultInline(admin.TabularInline):
    model = IdentificationResult
    extra = 0
    readonly_fields = ("bird", "confidence", "time_start", "time_end")
    ordering = ("-confidence",)
    can_delete = False


@admin.register(IdentificationReport)
class IdentificationReportAdmin(admin.ModelAdmin):
    list_display = ("id", "submitted_by", "status", "result_count", "created_at")
    list_filter = ("status",)
    search_fields = ("submitted_by__username", "submitted_by__email")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    inlines = (IdentificationResultInline,)

    @admin.display(description="Results")
    def result_count(self, obj):
        return obj.results.count()


@admin.register(IdentificationResult)
class IdentificationResultAdmin(admin.ModelAdmin):
    list_display = ("report", "bird", "confidence", "time_start", "time_end")
    list_filter = ("bird",)
    search_fields = ("bird__common_name", "bird__scientific_name", "report__id")
    ordering = ("-confidence",)
    list_select_related = ("bird", "report")
