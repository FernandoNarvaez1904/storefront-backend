from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('graphql', AsyncGraphQLView.as_view(schema=schema)),
]
