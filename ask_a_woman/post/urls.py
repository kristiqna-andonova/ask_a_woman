from django.urls import path, include

from ask_a_woman.post import views


urlpatterns = [
    path('create-post/', views.CreatePostView.as_view(), name='create-post'),
path('<str:type>/', views.FilteredPostsView.as_view(), name='filter-posts'),
    path('<int:pk>/', include([
        path('post-details/', views.PostDetailView.as_view(), name='post-details'),
        path('post-delete/', views.PostDeleteView.as_view(), name='post-delete'),
        path('post-edit/', views.EditPostView.as_view(), name='post-edit'),
        path('comment/', views.comment_functionality, name='comment-functionality'),
        path('bookmark/', views.bookmark_functionality, name='bookmark-functionality'),
        path('comment/delete/<int:comment_id>/', views.DeleteCommentView.as_view(), name='delete-comment'),
    ]))
]
