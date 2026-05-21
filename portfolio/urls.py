from django.urls import path
from portfolio.views import index_view, fetch_asset_view, side_ventures_api

app_name = 'portfolio'

urlpatterns = [
    # Primary Singular Workspace Entry
    path('', index_view, name='home'),
    path('index/', index_view, name='index'),

    # Knowledge Vault — Dual-Source Secure Asset Stream
    path('vault/asset/<int:asset_id>/', fetch_asset_view, name='fetch_knowledge_asset'),

    # Side Ventures API
    path('api/side-ventures/', side_ventures_api, name='side_ventures_api'),
]

