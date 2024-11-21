from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from ask_a_woman.account.models import Profile
from ask_a_woman.common.forms import CommentForm
from ask_a_woman.common.models import Comment, Bookmark
from ask_a_woman.post.forms import CreatePostForm, DeletePost, EditPostForm
from ask_a_woman.post.models import Post


# Create your views here.


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')  # Specify the login URL if not already set in settings
    redirect_field_name = 'redirect_to'  # Optional: specify redirect field
    success_url = reverse_lazy('home')
    template_name = 'posts/create-form.html'
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'posts/post_details.html'
#     login_url = reverse_lazy('login')
#     context_object_name = 'posts'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.object
#         user = self.request.user
#
#             # Check if the current user has liked the post
#         if user.is_authenticated:
#             for post in context['posts']:
#                 post.has_liked = post.like_set.filter(user=user).exists()
#
#             # Fetch comments using the correct field name 'to_post'
#         comments = Comment.objects.filter(to_post=post).order_by('-date_time_of_publication')
#
#             # Add additional context variables
#         context.update({
#             'show_delete_icon': self.request.user == post.author,  # Only show delete icon for the author
#             'show_edit_icon': self.request.user == post.author,  # Only show edit icon for the author
#             'post': post,
#             'comments': comments,
#             'comment_form': CommentForm()
#         })
#
#         return context
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_details.html'
    login_url = reverse_lazy('login')
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object  # This is the current post being viewed
        user = self.request.user

        # Check if the user is authenticated and set the 'has_liked' attribute
        if user.is_authenticated:
            post.has_liked = post.like_set.filter(user=user).exists()
            post.has_bookmarked = Bookmark.objects.filter(user=user, post=post).exists()

        # Fetch comments for this post
        comments = Comment.objects.filter(to_post=post).order_by('-date_time_of_publication')

        context.update({
            'show_delete_icon': self.request.user == post.author,  # Show delete icon only for the post author
            'show_edit_icon': self.request.user == post.author,  # Show edit icon only for the post author
            'comments': comments,
            'comment_form': CommentForm(),  # Provide the empty comment form for new comments
        })

        return context
def bookmark_functionality(request, pk):
    if not request.user.is_authenticated:
        # Redirect to login page if the user is not authenticated
        return redirect('login')
    post = get_object_or_404(Post, pk=pk)

    # Check if the post is already bookmarked by the user
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

    if not created:  # If it's already bookmarked, remove it (unbookmark)
        bookmark.delete()

    return redirect(request.META.get('HTTP_REFERER'))

def comment_functionality(request, pk):
    if not request.user.is_authenticated:
        # Redirect to login page if the user is not authenticated
        return redirect('login')
    if request.method == 'POST':  # Only allow POST requests
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_post = post  # Link the comment to the current post
            comment.user = request.user  # Set the user as the current logged-in user
            comment.save()

        # After saving the comment, redirect back to the same post detail page
        return redirect(request.META.get('HTTP_REFERER') + f'#{post.id}')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    form_class = DeletePost
    template_name = 'posts/delete-post.html'

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)

        return context

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '')
        post_details_url = reverse('post-details', kwargs={'pk': self.object.pk})
        home_url = reverse('home')  # Replace 'home-page' with your home view's URL name

        # If the referer contains 'post-details', return there; otherwise, go to home
        if 'post-details' in referer:
            return post_details_url
        else:
            return home_url


class EditPostView(UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'posts/edit-post.html'

    def get_success_url(self):
        # Get the 'next' parameter from the form data
        next_url = self.request.POST.get('next')

        # If the 'next' parameter exists, redirect to that URL
        if next_url:
            return next_url

        # Fallback: If 'next' is not provided, redirect to the home page
        return reverse('home')  # Replace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context


class FilteredPostsView(ListView):
    model = Post
    template_name = 'posts/filtered_posts.html'  # New template for filtered posts
    context_object_name = 'posts'
    paginate_by = 3  # No pagination, to allow infinite scroll

    def get_queryset(self):

        # Get the 'type' parameter from the URL (if available)
        post_type = self.kwargs.get('type', None)

        if post_type:
            # Filter the posts based on the type from the URL
            return Post.objects.filter(type=post_type).order_by('-created_at')

        # If no 'type' parameter, return all posts
        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['comment_form'] = CommentForm()

        # Check if the current user has liked the post
        if user.is_authenticated:
            for post in context['posts']:
                post.has_liked = post.like_set.filter(user=user).exists()

        return context


