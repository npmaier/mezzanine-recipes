"""
Default settings for the ``mezzanine_recipe`` app. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.

Thought should be given to how a setting is actually used before
making it editable, as it may be inappropriate - for example settings
that are only read during startup shouldn't be editable, since changing
them would require an application reload.
"""

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
    name="ADMIN_MENU_ORDER",
    description=_("Controls the ordering and grouping of the admin menu."),
    editable=False,
    default=(
        (_("Content"), ("pages.Page", "mezzanine_recipes.BlogPost", "mezzanine_recipes.Recipe",
                        "generic.ThreadedComment", (_("Media Library"), "fb_browse"),)),
        (_("Site"), ("sites.Site", "redirects.Redirect", "conf.Setting")),
        (_("Users"), ("auth.User", "auth.Group",)),
        (_("REST Service"), ("tastypie.ApiKey", "tastypie.ApiAccess",)),
    ),
)

register_setting(
    name="BLOG_SLUG",
    description=_("Slug of the page object for the blog."),
    editable=False,
    default="blog",
)

register_setting(
    name="RECIPES_SLUG",
    description=_("Slug of the page object for the blog."),
    editable=False,
    default="recipes",
)

register_setting(
    name="ARTICLES_SLUG",
    description=_("Slug of the page object for the blog."),
    editable=False,
    default="articles",
)