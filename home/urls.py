from django.urls import path

from home.views import BlogView, CommentView

urlpatterns = [
    path('blog/', BlogView.as_view(), name='blog-list'),
    path('blog/<uuid:post_id>/comments/', CommentView.as_view(), name='comment-list'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/', CommentView.as_view(), name='comment-detail'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/reply/', CommentView.as_view(), name='comment-reply'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/reply/<uuid:reply_id>/', CommentView.as_view(), name='comment-reply-detail'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/like/', CommentView.as_view(), name='comment-like'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/dislike/', CommentView.as_view(), name='comment-dislike'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/report/', CommentView.as_view(), name='comment-report'),
    path('blog/<uuid:post_id>/comments/<uuid:comment_id>/delete/', CommentView.as_view(), name='comment-delete'),
]
