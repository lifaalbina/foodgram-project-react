from django.contrib import admin
from django.urls import path, include
from api.views import TagViewSet, IngredientViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),
    path('api/tags/', TagViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/ingredients/', IngredientViewSet.as_view({'get': 'list', 'post': 'create'}))
]
