from django.contrib import admin
from .models import Article, Section, Athlete


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1


class AthleteInline(admin.TabularInline):
    model = Athlete
    extra = 1


@admin.register(Article)
class SportHistoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SectionInline, AthleteInline]


admin.site.register(Section)
admin.site.register(Athlete)
