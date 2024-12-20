from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages

from ask_a_woman.account.models import Profile
from ask_a_woman.account.forms import UpdateForm, CustomUserForm, CustomPasswordChangeForm, ProfilePicForm
from ask_a_woman.common.models import Bookmark
from ask_a_woman.post.models import Post

UserModel = get_user_model()

class UserRegisterView(CreateView):
    form_class = CustomUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)

        return  response

def profile_details(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    posts = Post.objects.filter(author_id=pk).order_by('-created_at')
    bookmarked_posts = None
    if request.user.is_authenticated and request.user == profile.user:
        bookmarked_posts = Bookmark.objects.filter(user=request.user).select_related('post').order_by('-created_at')

    if request.user.is_authenticated:
        for post in posts:
            post.has_liked = post.like_set.filter(user=request.user).exists()
            post.has_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        current_profile = request.user.profile
        action = request.POST.get('follow', '')

        if action == "unfollow":
            current_profile.follows.remove(profile)
        elif action == "follow":
            current_profile.follows.add(profile)

        current_profile.save()

        if 'bookmark' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, pk=post_id)
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
            if not created:
                bookmark.delete()

            return JsonResponse({
                'is_bookmarked': created
            })

    context = {
        "profile": profile,
        "posts": posts,
        "bookmarked_posts": bookmarked_posts,
        "show_delete_icon": request.user.is_authenticated,
        "show_edit_icon": request.user.is_authenticated,
    }

    return render(request, 'profile/profile_details.html', context)



class UserProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = UpdateForm
    template_name = 'profile/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user=self.request.user)
        context['profile_form'] = ProfilePicForm(instance=user_profile)
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        current_user = self.request.user
        if email:
            User = get_user_model()
            if User.objects.filter(email=email).exclude(pk=current_user.pk).exists():
                form.add_error('email', "This email is already in use. Please choose a different one.")
                return self.form_invalid(form)

        # Save the user form
        user_instance = form.save()

        # Handle the profile form
        profile_form = ProfilePicForm(self.request.POST, self.request.FILES,
                                      instance=Profile.objects.get(user=user_instance))
        if profile_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user_instance
            profile_instance.save()

            messages.success(self.request, "Your profile has been updated!")
            return redirect(reverse("profile-details", kwargs={'pk': current_user.id}))

        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))


def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to change your password.")
        return redirect('login')

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()

            login(request, request.user)

            update_session_auth_hash(request, request.user)
            login(request, request.user)

            messages.success(request, "Your password has been changed successfully!")
            return redirect(reverse_lazy('profile-details', kwargs={'pk': request.user.id}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'profile/change_password.html', {'form': form})

class DeleteUserProfile(DeleteView):
    model = get_user_model()
    template_name = 'profile/delete_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset = None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile

        profile.delete()