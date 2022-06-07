from django.urls import path
from strawberry.django.views import AsyncGraphQLView

from storefront_backend.api.schema import schema

# Probando Clickup
urlpatterns = [
    path('graphql', AsyncGraphQLView.as_view(schema=schema)),
]
