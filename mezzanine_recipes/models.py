from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from mezzanine.conf import settings
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

    def _get_next_or_previous_by_publish_date(self, is_next, **kwargs):
        """
        Retrieves next or previous object by publish date. We implement
        our own version instead of Django's so we can hook into the
        published manager and concrete subclasses.
        """
        arg = "publish_date__gt" if is_next else "publish_date__lt"
        order = "publish_date" if is_next else "-publish_date"
        lookup = {arg: self.publish_date}
        concrete_model = self.__class__
        try:
            queryset = concrete_model.secondary.published
        except AttributeError:
            queryset = concrete_model.secondary.all
        try:
            return queryset(**kwargs).filter(**lookup).order_by(order)[0]
        except IndexError:
            pass


class BlogPost(BlogProxy):
    secondary = BlogManager()

    @models.permalink
    def get_absolute_url(self):
        url_name = "blog_post_detail"
        kwargs = {"slug": "%s/%s" % (settings.ARTICLES_SLUG, self.slug)}
        if settings.BLOG_URLS_USE_DATE:
            url_name = "blog_post_detail_date"
            month = str(self.publish_date.month)
            if len(month) == 1:
                month = "0" + month
            day = str(self.publish_date.day)
            if len(day) == 1:
                day = "0" + day
            kwargs.update({
                "day": day,
                "month": month,
                "year": self.publish_date.year,
                })
        return (url_name, (), kwargs)

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

    @models.permalink
    def get_absolute_url(self):
        url_name = "blog_post_detail"
        kwargs = {"slug": "%s/%s" % (settings.RECIPES_SLUG, self.slug)}
        if settings.BLOG_URLS_USE_DATE:
            url_name = "blog_post_detail_date"
            month = str(self.publish_date.month)
            if len(month) == 1:
                month = "0" + month
            day = str(self.publish_date.day)
            if len(day) == 1:
                day = "0" + day
            kwargs.update({
                "day": day,
                "month": month,
                "year": self.publish_date.year,
                })
        return (url_name, (), kwargs)

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
        _ingredient = u'%s' % (self.ingredient)

        if self.unit:
            _ingredient = u'%s %s' % (self.get_unit_display(), _ingredient)

        if self.quantity:
            _ingredient = u'%s %s' % (self.quantity, _ingredient)

        if len(self.note):
           _ingredient = u'%s - %s' % (_ingredient, self.note)

        return _ingredient

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")


class Period(models.Model):
    """
    Provides fields for a period of time
    """
    hours = models.IntegerField(_("hours"), default=0)
    minutes = models.IntegerField(_("minutes"), default=0)

    def __unicode__(self):
        return "%02d:%02d" %(self.hours, self.minutes)

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

    def __unicode__(self):
        period = super(RestPeriod, self).__unicode__()
        return "%02d:%s" %(self.days, period)

    class Meta:
        verbose_name = _("rest period")
        verbose_name_plural = verbose_name
