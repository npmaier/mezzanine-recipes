from django.shortcuts import get_object_or_404

from mezzanine.blog import views as blog_views
from mezzanine.utils.views import render

from .models import Recipe


def blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html"):
    return blog_views.blog_post_list(request, tag, year, month, username, category, template)


def blog_post_detail(request, slug, year=None, month=None, day=None, template="recipe/blog_post_detail.html"):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    blog_posts = Recipe.objects.published(for_user=request.user)
    try:
        blog_post = get_object_or_404(blog_posts, slug=slug)
    except:
        return blog_views.blog_post_detail(request, slug, year, month, day)
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    templates = [u"blog/blog_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)


def blog_post_feed(request, format, **kwargs):
    return blog_views.blog_post_feed(request, format, **kwargs)


