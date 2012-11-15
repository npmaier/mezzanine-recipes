from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Orderable
from mezzanine.blog.models import BlogPost

from . import fields


class Recipe(BlogPost):
    """
    Implements the recipe type of page with all recipe fields.
    """
    summary = models.TextField(_("Summary"), blank=True, null=True)
    portions = models.IntegerField(_("Portions"), blank=True, null=True)
    difficulty = models.IntegerField(_("Difficulty"), choices=fields.DIFFICULTIES, blank=True, null=True)
    source = models.URLField(_("Source"), blank=True, null=True, help_text=_("URL of the source recipe"))

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
