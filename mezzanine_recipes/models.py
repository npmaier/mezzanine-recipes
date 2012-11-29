from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from mezzanine.core.models import Orderable
from mezzanine.core.managers import DisplayableManager
from mezzanine.blog.models import BlogPost as MezzanineBlogPost
from mezzanine.utils.timezone import now

from . import fields


class SubclassingQuerySet(QuerySet):

    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, BlogProxy) :
            return result.as_leaf_class()
        else :
            return result

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class BlogManager(DisplayableManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)



class BlogProxy(MezzanineBlogPost):
    content_type = models.ForeignKey(ContentType,editable=False,null=True)
    modified_date = models.DateTimeField(_("Last Modified"), blank=True, null=True)

    template_dir = "blog/"
    secondary = BlogManager()

    def save(self, *args, **kwargs):
        self.modified_date = now()
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(BlogProxy, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if model == BlogProxy:
            return self
        return model.objects.get(id=self.id)


class BlogPost(BlogProxy):
    secondary = BlogManager()

    class Meta:
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")
        ordering = ("-publish_date",)


class Recipe(BlogProxy):
    """
    Implements the recipe type of page with all recipe fields.
    """
    summary = models.TextField(_("Summary"), blank=True, null=True)
    portions = models.IntegerField(_("Portions"), blank=True, null=True)
    difficulty = models.IntegerField(_("Difficulty"), choices=fields.DIFFICULTIES, blank=True, null=True)
    source = models.URLField(_("Source"), blank=True, null=True, help_text=_("URL of the source recipe"))

    template_dir = "recipe/"
    secondary = BlogManager()
    search_fields = ("title", "summary", "description",)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ("-publish_date",)


class Ingredient(Orderable):
    """
    Provides ingredient fields for managing recipe content and making
    it searchable.
    """
    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"), related_name="ingredients")
    quantity = models.CharField(_("Quantity"), max_length=10, blank=True, null=True)
    unit = models.IntegerField(_("Unit"), choices=fields.UNITS, blank=True, null=True)
    ingredient = models.CharField(_("Ingredient"), max_length=100)
    note = models.CharField(_("Note"), max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.ingredient)

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")


class Period(models.Model):
    """
    Provides fields for a period of time
    """
    hours = models.IntegerField(_("hours"), default=0)
    minutes = models.IntegerField(_("minutes"), default=0)

    class Meta:
        abstract = True


class WorkingHours(Period):
    """
    Provides working hour fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="working_hours")

    class Meta:
        verbose_name = _("working hour")
        verbose_name_plural = verbose_name


class CookingTime(Period):
    """
    Provides cooking time fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="cooking_time")

    class Meta:
        verbose_name = _("cooking time")
        verbose_name_plural = verbose_name


class RestPeriod(Period):
    """
    Provides rest time fields for cooking a recipe
    """
    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"), related_name="rest_period")
    days = models.IntegerField(_("days"), default=0)

    class Meta:
        verbose_name = _("rest period")
        verbose_name_plural = verbose_name
