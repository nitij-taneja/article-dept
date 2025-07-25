from django.db import models
import uuid

class ArticleSearchResult(models.Model):
    """Model to store article search results"""
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ar', 'Arabic'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1000)
    snippet = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    search_query = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.language})"

class ArticleContent(models.Model):
    """Model to store fetched article content"""
    
    search_result = models.OneToOneField(ArticleSearchResult, on_delete=models.CASCADE, related_name='content')
    full_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    keywords = models.JSONField(default=list, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Content for: {self.search_result.title}"

