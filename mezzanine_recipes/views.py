from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog import views as blog_views
from mezzanine.utils.views import render

from .models import BlogProxy


def blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html"):
    return blog_views.blog_post_list(request, tag, year, month, username, category, template)


def blog_post_detail(request, slug, year=None, month=None, day=None, template="blog_post_detail.html"):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """

    blog_posts = BlogProxy.objects.published(for_user=request.user).filter(slug=slug)
    if len(blog_posts) != 1:
        raise Http404(_('Slug %s does not exist.' % slug))
    blog_post = blog_posts[0]
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    templates = [u"%sblog_post_detail_%s.html" % (blog_post.template_dir, unicode(slug)), u"%s%s" % (blog_post.template_dir, template)]
    return render(request, templates, context)


def blog_post_feed(request, format, **kwargs):
    return blog_views.blog_post_feed(request, format, **kwargs)


