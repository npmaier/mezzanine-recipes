from copy import deepcopy
from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin, DisplayableAdmin, OwnableAdmin
from .models import Recipe, Ingredient, WorkingHours, CookingTime, RestPeriod, RecipeCategory


recipe_extra_fieldsets = ((None, {"fields": ("cover", "summary", "categories", "content", "portions", "difficulty", "source", "allow_comments",)}),)


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours

class CookingTimeInline(admin.TabularInline):
    model = CookingTime

class RestPeriodInline(admin.TabularInline):
    model = RestPeriod
    fields = ("days", "hours", "minutes",)

class IngredientInline(TabularDynamicInlineAdmin):
    model = Ingredient


class RecipeAdmin(PageAdmin, OwnableAdmin):
    """
    Admin class for recipes.
    """

    inlines = (IngredientInline, WorkingHoursInline, CookingTimeInline, RestPeriodInline,)
    fieldsets = deepcopy(PageAdmin.fieldsets) + recipe_extra_fieldsets
    filter_horizontal = ("categories",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class RecipeCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for recipe categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu.
        """
        return False

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)