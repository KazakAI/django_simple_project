from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone


POST_AMT = 5


def valid_posts_query():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    )


def index(request):
    template_name = 'blog/index.html'
    all_posts = valid_posts_query()[:POST_AMT]
    context = {'post_list': all_posts}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post_data = get_object_or_404(valid_posts_query(), id=post_id)

    context = {'post': post_data}

    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    context = {'category': category_slug}

    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    all_posts = valid_posts_query().filter(category=category)

    context = {
        'category': category,
        'post_list': all_posts
    }

    return render(request, template_name, context)
