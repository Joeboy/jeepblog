from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.http import HttpResponseNotFound
from jeepblog.blog.models import Post, Category

@cache_page(60*1)
def index(request):
    return render_to_response("blog/index.html",
                              {'categories': Category.objects.filter(parent=None)},
                              context_instance=RequestContext(request))


@cache_page(60 * 1)
def blog_entry(request, blog_path):
    # This may be a link to a post or to a category:
    path_end = blog_path.split('/')[-1]
    if Post.objects.filter(slug=path_end, published=True):
        return render_to_response( 'blog/post.html',
                                   {'post':get_object_or_404(Post, slug=path_end, published=True),},
                                   context_instance=RequestContext(request) )
    elif Category.objects.filter(slug=path_end):
        return render_to_response( 'blog/category.html',
                                   {'category':get_object_or_404(Category, slug=path_end),},
                                   context_instance=RequestContext(request) )
    else:
        return HttpResponseNotFound("Sorry, couldn't find that.")

