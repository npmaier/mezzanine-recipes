from django.utils.translation import ugettext_lazy as _
from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.fields import FileField
from mezzanine.core.models import RichText, Slugged, Ownable, Orderable
from mezzanine.generic.fields import CommentsField
from mezzanine.utils.models import AdminThumbMixin
from . import fields


class Recipe(Page, Ownable, RichText, AdminThumbMixin):
    """
    Implements the recipe type of page with all recipe fields.
    """

    cover = FileField(verbose_name=_("Cover Image"), upload_to="rawfoodimages", format="Image", max_length=255, null=True, blank=True)
    summary = models.CharField(_("Summary"), max_length=200, blank=True, null=True)
    portions = models.IntegerField(_("Portions"), blank=True, null=True)
    difficulty = models.IntegerField(_("Difficulty"), choices=fields.DIFFICULTIES, blank=True, null=True)
    source = models.URLField(_("Source"), blank=True, null=True, help_text=_("URL of the source recipe"))
    categories = models.ManyToManyField("RecipeCategory", verbose_name=_("Categories"), blank=True, related_name="recipes")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"), default=True)
    comments = CommentsField(verbose_name=_("Comments"))

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ("-publish_date",)


class RecipeCategory(Slugged):
    """
    A category for grouping blog posts into a series.
    """

    class Meta:
        verbose_name = _("Recipe Category")
        verbose_name_plural = _("Recipe Categories")

    @models.permalink
    def get_absolute_url(self):
        return ("recipe_post_list_category", (), {"slug": self.slug})


class Ingredient(Orderable):
    """
    Provides ingredient fields for managing recipe content and making
    it searchable.
    """

    recipe = models.ForeignKey("Recipe", verbose_name=_("Recipe"))
    quantity = models.CharField(_("Quantity"), max_length=10, blank=True, null=True)
    unit = models.IntegerField(_("Unit"), choices=fields.UNITS, blank=True, null=True)
    ingredient = models.CharField(_("Ingredient"), max_length=100)
    note = models.CharField(_("Note"), max_length=200, blank=True, null=True)

    search_fields = ("title",)

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

    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"))

    class Meta:
        verbose_name = _("working hour")
        verbose_name_plural = verbose_name


class CookingTime(Period):
    """
    Provides cooking time fields for cooking a recipe
    """

    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"))

    class Meta:
        verbose_name = _("cooking time")
        verbose_name_plural = verbose_name


class RestPeriod(Period):
    """
    Provides rest time fields for cooking a recipe
    """

    recipe = models.OneToOneField("Recipe", verbose_name=_("Recipe"))
    days = models.IntegerField(_("days"), default=0)

    class Meta:
        verbose_name = _("rest period")
        verbose_name_plural = verbose_name
