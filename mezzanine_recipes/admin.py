from copy import deepcopy
from django.contrib import admin

from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost as MezzanineBlogPost
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin, TabularDynamicInlineAdmin

from .models import Recipe, Ingredient, WorkingHours, CookingTime, RestPeriod, BlogPost


blogpost_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blogpost_fieldsets[0][1]["fields"].extend(["summary", "portions", "difficulty", "source",])
blogpost_fieldsets[0][1]["fields"].insert(-6, "featured_image")
recipe_list_display = deepcopy(BlogPostAdmin.list_display)
recipe_list_display.insert(0, "admin_thumb")

class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours

class CookingTimeInline(admin.TabularInline):
    model = CookingTime

class RestPeriodInline(admin.TabularInline):
    model = RestPeriod
    fields = ("days", "hours", "minutes",)

class IngredientInline(TabularDynamicInlineAdmin):
    model = Ingredient

class RecipeAdmin(BlogPostAdmin):
    """
    Admin class for recipes.
    """
    inlines = (IngredientInline, WorkingHoursInline, CookingTimeInline, RestPeriodInline,)
    fieldsets = blogpost_fieldsets
    list_display = recipe_list_display

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


admin.site.unregister(MezzanineBlogPost)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Recipe, RecipeAdmin)