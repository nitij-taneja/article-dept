from django.urls import path
from .views import ArticleSearchView, ArticleContentView, HealthCheckView, DepartmentInfoView

app_name = 'articles'

urlpatterns = [
    path('search/', ArticleSearchView.as_view(), name='article-search'),
    path('content/', ArticleContentView.as_view(), name='article-content'),
    path('department/', DepartmentInfoView.as_view(), name='department-info'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

