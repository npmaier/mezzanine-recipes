import re

from django.conf.urls.defaults import url
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import Http404
from django.utils import simplejson

from mezzanine.generic.models import ThreadedComment, AssignedKeyword, Keyword, Rating
from mezzanine.blog.models import BlogCategory
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.utils.timezone import now

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache
from tastypie.throttle import CacheDBThrottle
from tastypie.utils import trailing_slash
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField

from .models import BlogProxy, Recipe, BlogPost, Ingredient, WorkingHours, CookingTime, RestPeriod
from .fields import DIFFICULTIES, UNITS


class CamelCaseJSONSerializer(Serializer):
    formats = ['json']
    content_types = {
        'json': 'application/json',
        }

    def to_json(self, data, options=None):
        # Changes underscore_separated names to camelCase names to go from python convention to javacsript convention
        data = self.to_simple(data, options)

        def underscoreToCamel(match):
            return match.group()[0] + match.group()[2].upper()

        def camelize(data):
            if isinstance(data, dict):
                new_dict = {}
                for key, value in data.items():
                    new_key = re.sub(r"[a-z]_[a-z]", underscoreToCamel, key)
                    new_dict[new_key] = camelize(value)
                return new_dict
            if isinstance(data, (list, tuple)):
                for i in range(len(data)):
                    data[i] = camelize(data[i])
                return data
            return data

        camelized_data = camelize(data)

        return simplejson.dumps(camelized_data, sort_keys=True)

    def from_json(self, content):
        # Changes camelCase names to underscore_separated names to go from javascript convention to python convention
        data = simplejson.loads(content)

        def camelToUnderscore(match):
            return match.group()[0] + "_" + match.group()[1].lower()

        def underscorize(data):
            if isinstance(data, dict):
                new_dict = {}
                for key, value in data.items():
                    new_key = re.sub(r"[a-z][A-Z]", camelToUnderscore, key)
                    new_dict[new_key] = underscorize(value)
                return new_dict
            if isinstance(data, (list, tuple)):
                for i in range(len(data)):
                    data[i] = underscorize(data[i])
                return data
            return data

        underscored_data = underscorize(data)

        return underscored_data



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
        serializer = CamelCaseJSONSerializer()

    def get_object_list(self, request, *args, **kwargs):
        return BlogCategory.objects.filter(Q(blogposts__publish_date__lte=now()) | Q(blogposts__publish_date__isnull=True),
                                           Q(blogposts__expiry_date__gte=now()) | Q(blogposts__expiry_date__isnull=True),
                                           Q(blogposts__status=CONTENT_STATUS_PUBLISHED)).distinct()



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
        serializer = CamelCaseJSONSerializer()

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
        serializer = CamelCaseJSONSerializer()

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
        serializer = CamelCaseJSONSerializer()

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



class CommentResource(ModelResource):
    replied_to = fields.ToOneField('mezzanine_recipes.api.CommentResource', 'replied_to', null=True)
    post = GenericForeignKeyField({
        BlogProxy: PostResource,
        BlogPost: BlogPostResource,
        Recipe: RecipeResource
    }, 'content_object')

    class Meta:
        queryset = ThreadedComment.objects.visible()
        resource_name = "comments"
        fields = ['id', 'comment', 'submit_date', 'user_name', 'user_email', 'user_url', 'replied_to',]
        list_allowed_methods = ['get', 'post',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            'object_pk': ('exact',),
            }
        serializer = CamelCaseJSONSerializer()
        authorization = Authorization()

    def dehydrate_user_email(self, bundle):
        return None

    def dehydrate_user_url(self, bundle):
        return None



class RatingResource(ModelResource):
    post = GenericForeignKeyField({
        BlogProxy: PostResource,
        BlogPost: BlogPostResource,
        Recipe: RecipeResource
    }, 'content_object')

    class Meta:
        queryset = Rating.objects.all()
        resource_name = "rating"
        fields = ['id', 'value',]
        list_allowed_methods = ['get', 'post',]
        detail_allowed_methods = ['get',]
        cache = SimpleCache()
        throttle = CacheDBThrottle()
        filtering = {
            'object_pk': ('exact',),
            }
        serializer = CamelCaseJSONSerializer()
        authorization = Authorization()



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
        serializer = CamelCaseJSONSerializer()



class AssignedKeywordResource(ModelResource):
    assignments = fields.ToOneField('mezzanine_recipes.api.KeywordResource', 'keyword', full=True)
    post = GenericForeignKeyField({
        BlogProxy: PostResource,
        BlogPost: BlogPostResource,
        Recipe: RecipeResource
    }, 'content_object')

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
        serializer = CamelCaseJSONSerializer()



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
        serializer = CamelCaseJSONSerializer()

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
        serializer = CamelCaseJSONSerializer()

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
        serializer = CamelCaseJSONSerializer()

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
        serializer = CamelCaseJSONSerializer()

    def get_object_list(self, request, *args, **kwargs):
        return RestPeriod.objects.filter(Q(recipe__publish_date__lte=now()) | Q(recipe__publish_date__isnull=True),
                                         Q(recipe__expiry_date__gte=now()) | Q(recipe__expiry_date__isnull=True),
                                         Q(recipe__status=CONTENT_STATUS_PUBLISHED))