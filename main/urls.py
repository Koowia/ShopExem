from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('catalog/', views.CatalogView.as_view(), name='catalog_all'),
    path('catalog/', views.CatalogIndexView.as_view(), name='catalog_index'),
    path('catalog/<slug:category_slug>/', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.CatalogView.as_view(), name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]