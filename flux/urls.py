from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import flux, posts, create_ticket, \
    create_review, create_review_ticket, \
    edit_review, edit_ticket, \
    follow_users, delete_follow

urlpatterns = [
    path('flux/', flux, name='flux'),
    path('posts/', posts, name='posts'),
    path('createticket/', create_ticket, name='create_ticket'),
    path('<int:ticket_id>/createreview/', create_review, name='create_review'),
    path('createreviewticket/', create_review_ticket, name='create_review_ticket'),
    path("<int:ticket_id>/editticket/", edit_ticket, name="edit_ticket"),
    path("<int:review_id>/editreview/", edit_review, name="edit_review"),
    path("followusers/", follow_users, name="follow_users"),
    path("delete_follow/<int:user_id>", delete_follow, name="delete_follow"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
