from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from ask_a_woman.account.models import Profile
from ask_a_woman.common.forms import CommentForm
from ask_a_woman.common.models import Comment, Bookmark
from ask_a_woman.post.forms import CreatePostForm, DeletePost, EditPostForm
from ask_a_woman.post.models import Post



class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('home')
    template_name = 'posts/create-form.html'
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_details.html'
    login_url = reverse_lazy('login')
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user

        if user.is_authenticated:
            post.has_liked = post.like_set.filter(user=user).exists()
            post.has_bookmarked = Bookmark.objects.filter(user=user, post=post).exists()

        comments = Comment.objects.filter(to_post=post).order_by('-date_time_of_publication')

        context.update({
            'show_delete_icon': self.request.user == post.author,
            'show_edit_icon': self.request.user == post.author,
            'comments': comments,
            'comment_form': CommentForm(),
        })

        return context
def bookmark_functionality(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, pk=pk)

    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

    if not created:
        bookmark.delete()

    return redirect(request.META.get('HTTP_REFERER'))

def comment_functionality(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_post = post
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{post.id}')

class PostDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Post
    form_class = DeletePost
    template_name = 'posts/delete-post.html'

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '')
        post_details_url = reverse('post-details', kwargs={'pk': self.object.pk})
        home_url = reverse('home')

        if 'post-details' in referer:
            return post_details_url
        else:
            return home_url

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)

        return context

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class EditPostView(UpdateView, UserPassesTestMixin, LoginRequiredMixin):
    model = Post
    form_class = EditPostForm
    template_name = 'posts/edit-post.html'

    def get_success_url(self):
        next_url = self.request.POST.get('next')

        if next_url:
            return next_url

        return reverse('home')  # Replace

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context

    def handle_no_permission(self):
        return render(self.request, '403.html', status=403)


class FilteredPostsView(ListView):
    model = Post
    template_name = 'posts/filtered_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):

        post_type = self.kwargs.get('type', None)

        if post_type:
            return Post.objects.filter(type=post_type).order_by('-created_at')

        return Post.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['comment_form'] = CommentForm()


        if user.is_authenticated:
            for post in context['posts']:
                post.has_liked = post.like_set.filter(user=user).exists()
                post.has_bookmarked = Bookmark.objects.filter(user=user, post=post).exists()


        return context


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, pk, comment_id):

        post = get_object_or_404(Post, id=pk)
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user == comment.user or request.user == post.author:
            comment.delete()
            return redirect('post-details', pk=post.id)
        else:

            return HttpResponseForbidden("You are not allowed to delete this comment.")
