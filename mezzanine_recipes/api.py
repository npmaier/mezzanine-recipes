from django.db.models import Q
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.utils.timezone import now
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache
from tastypie.throttle import CacheDBThrottle
from .models import Recipe, RecipeCategory, Ingredient, WorkingHours, CookingTime, RestPeriod
from .fields import DIFFICULTIES, UNITS


class RecipeCategoryResource(ModelResource):
    recipes = fields.ToManyField('mezzanine_recipes.api.RecipeResource', 'recipes')

    class Meta:
        queryset = RecipeCategory.objects.all()
        resource_name = "categories"
        fields = ['id', 'title',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        limit = 0
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return RecipeCategory.objects.filter(Q(recipes__publish_date__lte=now()) | Q(recipes__publish_date__isnull=True),
                                             Q(recipes__expiry_date__gte=now()) | Q(recipes__expiry_date__isnull=True),
                                             Q(recipes__status=CONTENT_STATUS_PUBLISHED)).distinct()


class RecipeResource(ModelResource):
    categories = fields.ToManyField('mezzanine_recipes.api.RecipeCategoryResource', 'categories')
    ingredients = fields.ToManyField('mezzanine_recipes.api.IngredientResource', 'ingredients')
    working_hours = fields.ToOneField('mezzanine_recipes.api.WorkingHoursResource', 'working_hours', null=WorkingHours)
    cooking_time = fields.ToOneField('mezzanine_recipes.api.CookingTimeResource', 'cooking_time', null=CookingTime)
    rest_period = fields.ToOneField('mezzanine_recipes.api.RestPeriodResource', 'rest_period', null=RestPeriod)

    class Meta:
        queryset = Recipe.objects.published()
        resource_name = "recipe"
        fields = ['id', 'title', 'cover', 'summary', 'description', 'portions', 'difficulty',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def dehydrate_difficulty(self, bundle):
        return dict(DIFFICULTIES)[bundle.data['difficulty']]


class IngredientResource(ModelResource):
    recipe = fields.ToOneField('mezzanine_recipes.api.RecipeResource', 'recipe')

    class Meta:
        queryset = Ingredient.objects.all()
        resource_name = "ingredient"
        fields = ['id', 'recipe', 'quantity', 'unit', 'ingredient', 'note',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        limit = 0
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return Ingredient.objects.filter(Q(recipe__publish_date__lte=now()) | Q(recipe__publish_date__isnull=True),
                                         Q(recipe__expiry_date__gte=now()) | Q(recipe__expiry_date__isnull=True),
                                         Q(recipe__status=CONTENT_STATUS_PUBLISHED))

    def dehydrate_unit(self, bundle):
        return dict(UNITS)[bundle.data['unit']]


class WorkingHoursResource(ModelResource):
    recipe = fields.ToOneField('mezzanine_recipes.api.RecipeResource', 'recipe')

    class Meta:
        queryset = WorkingHours.objects.all()
        resource_name = "working_hours"
        fields = ['id', 'recipe', 'hours', 'minutes',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return WorkingHours.objects.filter(Q(recipe__publish_date__lte=now()) | Q(recipe__publish_date__isnull=True),
                                           Q(recipe__expiry_date__gte=now()) | Q(recipe__expiry_date__isnull=True),
                                           Q(recipe__status=CONTENT_STATUS_PUBLISHED))


class CookingTimeResource(ModelResource):
    recipe = fields.ToOneField('mezzanine_recipes.api.RecipeResource', 'recipe')

    class Meta:
        queryset = CookingTime.objects.all()
        resource_name = "cooking_time"
        fields = ['id', 'recipe', 'hours', 'minutes',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return CookingTime.objects.filter(Q(recipe__publish_date__lte=now()) | Q(recipe__publish_date__isnull=True),
                                          Q(recipe__expiry_date__gte=now()) | Q(recipe__expiry_date__isnull=True),
                                          Q(recipe__status=CONTENT_STATUS_PUBLISHED))


class RestPeriodResource(ModelResource):
    recipe = fields.ToOneField('mezzanine_recipes.api.RecipeResource', 'recipe')

    class Meta:
        queryset = RestPeriod.objects.all()
        resource_name = "rest_period"
        fields = ['id', 'recipe', 'days', 'hours', 'minutes',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return RestPeriod.objects.filter(Q(recipe__publish_date__lte=now()) | Q(recipe__publish_date__isnull=True),
                                         Q(recipe__expiry_date__gte=now()) | Q(recipe__expiry_date__isnull=True),
                                         Q(recipe__status=CONTENT_STATUS_PUBLISHED))