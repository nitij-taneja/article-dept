"""
URL configuration for article_search_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """Root API endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Article Search API',
        'version': '1.0.0',
        'endpoints': {
            'search': '/api/search/',
            'content': '/api/content/',
            'health': '/api/health/',
            'admin': '/admin/'
        },
        'documentation': {
            'search_endpoint': {
                'method': 'POST',
                'url': '/api/search/',
                'description': 'Search for articles by title with language support',
                'parameters': {
                    'query': 'string (required) - Search query',
                    'language': 'string (optional) - "en" or "ar", default: "en"',
                    'max_results': 'integer (optional) - Max results, default: 5'
                }
            },
            'content_endpoint': {
                'method': 'POST', 
                'url': '/api/content/',
                'description': 'Retrieve full article content by ID',
                'parameters': {
                    'article_id': 'UUID (required) - Article ID from search results',
                    'include_summary': 'boolean (optional) - Include AI summary, default: true'
                }
            }
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('articles.urls')),
    path('', api_root, name='api-root'),
]

