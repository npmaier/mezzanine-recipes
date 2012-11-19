from django.conf.urls.defaults import url
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import Http404

from mezzanine.generic.models import ThreadedComment, AssignedKeyword, Keyword
from mezzanine.blog.models import BlogCategory
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.utils.timezone import now

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache
from tastypie.throttle import CacheDBThrottle
from tastypie.utils import trailing_slash

from .models import BlogProxy, Recipe, BlogPost, Ingredient, WorkingHours, CookingTime, RestPeriod
from .fields import DIFFICULTIES, UNITS


class CategoryResource(ModelResource):
    recipes = fields.ToManyField('mezzanine_recipes.api.RecipeResource', 'blogposts')

    class Meta:
        queryset = BlogCategory.objects.all()
        resource_name = "categories"
        fields = ['id', 'title',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        limit = 0
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return BlogCategory.objects.filter(Q(blogposts__publish_date__lte=now()) | Q(blogposts__publish_date__isnull=True),
                                           Q(blogposts__expiry_date__gte=now()) | Q(blogposts__expiry_date__isnull=True),
                                           Q(blogposts__status=CONTENT_STATUS_PUBLISHED)).distinct()



class CommentResource(ModelResource):
    class Meta:
        queryset = ThreadedComment.objects.visible()
        resource_name = "comments"
        fields = ['id', 'comment', 'submit_date', 'user_name',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        limit = 0
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            'object_pk': ('exact',),
        }



class KeywordResource(ModelResource):
    keyword = fields.ToManyField('mezzanine_recipes.api.AssignedKeywordResource', 'assignments')

    class Meta:
        queryset = Keyword.objects.all()
        resource_name = "keywords"
        fields = ['id', 'title']
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        limit = 0
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            'title': ('exact',),
        }



class AssignedKeywordResource(ModelResource):
    assignments = fields.ToOneField('mezzanine_recipes.api.KeywordResource', 'keyword', full=True)

    class Meta:
        queryset = AssignedKeyword.objects.all()
        resource_name = "assigned_keywords"
        fields = ['id', '_order',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            'object_pk': ('exact',),
            }



class BlogPostResource(ModelResource):
    categories = fields.ToManyField('mezzanine_recipes.api.CategoryResource', 'categories', full=True)

    class Meta:
        queryset = BlogPost.objects.published().order_by('-publish_date')
        resource_name = "blog"
        fields = ['id', 'title', 'featured_image', 'description', 'publish_date', 'allow_comments', 'comments_count', 'rating_average', 'rating_count',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            "publish_date": ('gt',),
            }

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)

        sqs = BlogPost.objects.search(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404(_("Sorry, no results on that page."))

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
            }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)



class RecipeResource(ModelResource):
    categories = fields.ToManyField('mezzanine_recipes.api.CategoryResource', 'categories', full=True)
    ingredients = fields.ToManyField('mezzanine_recipes.api.IngredientResource', 'ingredients', full=True)
    working_hours = fields.ToOneField('mezzanine_recipes.api.WorkingHoursResource', 'working_hours', full=True, null=True)
    cooking_time = fields.ToOneField('mezzanine_recipes.api.CookingTimeResource', 'cooking_time', full=True, null=True)
    rest_period = fields.ToOneField('mezzanine_recipes.api.RestPeriodResource', 'rest_period', full=True, null=True)

    class Meta:
        queryset = Recipe.objects.published().order_by('-publish_date')
        resource_name = "recipe"
        fields = ['id', 'title', 'featured_image', 'summary', 'description', 'portions', 'difficulty', 'publish_date', 'allow_comments', 'comments_count', 'rating_average', 'rating_count',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            "publish_date": ('gt',),
            }

    def dehydrate_difficulty(self, bundle):
        return dict(DIFFICULTIES)[bundle.data['difficulty']]

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)

        sqs = Recipe.objects.search(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404(_("Sorry, no results on that page."))

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
            }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)



class PostResource(ModelResource):
    #categories = fields.ToManyField('mezzanine_recipes.api.CategoryResource', 'categories', full=True)

    class Meta:
        queryset = BlogProxy.secondary.published().order_by('-publish_date')
        resource_name = "post"
        fields = ['id', 'title', 'featured_image', 'description', 'publish_date', 'allow_comments', 'comments_count', 'rating_average', 'rating_count',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            "publish_date": ('gt',),
        }

    def dehydrate(self, bundle):
        if isinstance(bundle.obj, BlogPost):
            blog_res = BlogPostResource()
            rr_bundle = blog_res.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = blog_res.full_dehydrate(rr_bundle).data
        elif isinstance(bundle.obj, Recipe):
            recipe_res = RecipeResource()
            br_bundle = recipe_res.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = recipe_res.full_dehydrate(br_bundle).data
        return bundle

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)

        sqs = BlogProxy.secondary.search(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404(_("Sorry, no results on that page."))

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
            }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)



class IngredientResource(ModelResource):
    recipe = fields.ToOneField('mezzanine_recipes.api.RecipeResource', 'recipe')

    class Meta:
        queryset = Ingredient.objects.all()
        resource_name = "ingredient"
        fields = ['id', 'quantity', 'unit', 'ingredient', 'note',]
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
        fields = ['id', 'hours', 'minutes',]
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
        fields = ['id', 'hours', 'minutes',]
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
        fields = ['id', 'days', 'hours', 'minutes',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()

    def get_object_list(self, request, *args, **kwargs):
        return RestPeriod.objects.filter(Q(recipe__publish_date__lte=now()) | Q(recipe__publish_date__isnull=True),
                                         Q(recipe__expiry_date__gte=now()) | Q(recipe__expiry_date__isnull=True),
                                         Q(recipe__status=CONTENT_STATUS_PUBLISHED))