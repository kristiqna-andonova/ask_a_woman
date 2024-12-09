
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView

from ask_a_woman.account.models import Profile
from ask_a_woman.common.forms import CommentForm
from ask_a_woman.common.models import Like, Bookmark
from ask_a_woman.post.models import Post


# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['comment_form'] = CommentForm()

        if user.is_authenticated:
            for post in context['posts']:
                post.has_liked = post.like_set.filter(user=user).exists()
                post.has_bookmarked = Bookmark.objects.filter(user=user, post=post).exists()
        return context

def likes_functionality(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    liked_object = Like.objects.filter(
        to_post_id=pk,
        user=request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_post_id=pk, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{pk}')

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def search_results(request):
    query = request.GET.get('q', '')


    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) | Q(user__email__icontains=query)
    )
    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(user=request.user).values_list('to_post_id', flat=True)
        bookmarked_post_ids = Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)

        for post in posts:
            post.has_liked = post.id in liked_post_ids
            post.has_bookmarked = post.id in bookmarked_post_ids

    post_paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_page = post_paginator.get_page(page_number)


    profile_paginator = Paginator(profiles, 3)
    profile_page_number = request.GET.get('profile_page')
    profiles_page = profile_paginator.get_page(profile_page_number)

    context = {
        'query': query,
        'posts': posts_page,
        'profiles': profiles_page,
    }
    return render(request, 'search_results.html', context)


