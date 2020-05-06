from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .serializers import EmailAuthSerializer
from .views import (Auth, CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, UserViewSet)

v1_router = DefaultRouter()
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(r'users', UserViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/email/', Auth.send_confirmation_code),
    path('v1/auth/token/', TokenObtainPairView.as_view(serializer_class = EmailAuthSerializer), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls))
]
