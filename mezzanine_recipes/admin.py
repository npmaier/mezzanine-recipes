from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
#from django.conf import settings

from mezzanine.blog.admin import BlogPostAdmin as MezzanineBlogPostAdmin
from mezzanine.blog.models import BlogPost as MezzanineBlogPost
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.conf import settings

from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess

from .models import Recipe, Ingredient, WorkingHours, CookingTime, RestPeriod, BlogPost


blogpost_fieldsets = deepcopy(MezzanineBlogPostAdmin.fieldsets)
blogpost2_fieldsets = deepcopy(MezzanineBlogPostAdmin.fieldsets)
blogpost_fieldsets[0][1]["fields"].extend(["summary", "portions", "difficulty", "source"])
blogpost2_fieldsets[0][1]["fields"].extend(["modified_date"])
if not settings.BLOG_USE_FEATURED_IMAGE:
    blogpost_fieldsets[0][1]["fields"].insert(-6, "featured_image")
recipe_list_display = deepcopy(MezzanineBlogPostAdmin.list_display)
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

class RecipeAdmin(MezzanineBlogPostAdmin):
    """
    Admin class for recipes.
    """
    inlines = (IngredientInline, WorkingHoursInline, CookingTimeInline, RestPeriodInline,)
    fieldsets = blogpost_fieldsets
    list_display = recipe_list_display

class BlogPostAdmin(MezzanineBlogPostAdmin):
    fieldsets = blogpost2_fieldsets


admin.site.unregister(MezzanineBlogPost)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Recipe, RecipeAdmin)


class UserModelAdmin(UserAdmin):
    if 'tastypie' in settings.INSTALLED_APPS:
        inlines = UserAdmin.inlines + [ApiKeyInline]

if 'tastypie' in settings.INSTALLED_APPS:
    admin.site.register(ApiAccess)
    admin.site.unregister(User)
    admin.site.register(User, UserModelAdmin)