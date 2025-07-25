from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    """Serializer for article category information"""

    name = serializers.CharField()
    description = serializers.CharField()
    wikipedia_link = serializers.URLField()
    image = serializers.URLField()

class AuthorSerializer(serializers.Serializer):
    """Serializer for article author information"""

    name = serializers.CharField()
    profession = serializers.CharField()
    description = serializers.CharField()
    wikipedia_link = serializers.URLField()
    image = serializers.URLField()

class ArticleSearchResultSerializer(serializers.Serializer):
    """Serializer for LLM-generated article search results"""

    id = serializers.UUIDField()
    title = serializers.CharField()
    snippet = serializers.CharField()
    category = CategorySerializer()
    author = AuthorSerializer()
    language = serializers.CharField()
    search_query = serializers.CharField()

class ArticleContentSerializer(serializers.Serializer):
    """Serializer for LLM-generated article content"""

    id = serializers.UUIDField()
    full_text = serializers.CharField()
    summary = serializers.CharField()
    category = CategorySerializer()
    author = AuthorSerializer()
    keywords = serializers.ListField(child=serializers.CharField())
    publish_date = serializers.CharField()

class SearchRequestSerializer(serializers.Serializer):
    """Serializer for search request parameters"""
    
    query = serializers.CharField(max_length=200, help_text="Search query for articles")
    language = serializers.ChoiceField(
        choices=[('en', 'English'), ('ar', 'Arabic')], 
        default='en',
        help_text="Language for search results"
    )
    max_results = serializers.IntegerField(
        default=5, 
        min_value=1, 
        max_value=10,
        help_text="Maximum number of results to return"
    )

class SearchResponseSerializer(serializers.Serializer):
    """Serializer for search response"""
    
    success = serializers.BooleanField()
    message = serializers.CharField()
    results = ArticleSearchResultSerializer(many=True)
    total_count = serializers.IntegerField()

class ContentRequestSerializer(serializers.Serializer):
    """Serializer for content generation request"""

    article_id = serializers.UUIDField(help_text="UUID of the article to generate content for")
    query = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Original search query for context"
    )
    language = serializers.ChoiceField(
        choices=[('en', 'English'), ('ar', 'Arabic')],
        default='en',
        help_text="Language for content generation"
    )
    include_summary = serializers.BooleanField(
        default=True,
        help_text="Whether to include AI-generated summary"
    )

class ContentResponseSerializer(serializers.Serializer):
    """Serializer for content retrieval response"""

    success = serializers.BooleanField()
    message = serializers.CharField()
    content = ArticleContentSerializer(allow_null=True)

class DepartmentRequestSerializer(serializers.Serializer):
    """Serializer for department information request"""

    department = serializers.CharField(
        max_length=100,
        help_text="Department name or code (e.g., 'IT', 'Finance', 'Human Resources')"
    )
    language = serializers.ChoiceField(
        choices=[('en', 'English'), ('ar', 'Arabic')],
        default='en',
        help_text="Language for department information"
    )

class DepartmentInfoSerializer(serializers.Serializer):
    """Serializer for department information"""

    name = serializers.CharField()
    code = serializers.CharField()
    description = serializers.CharField()
    responsibilities = serializers.ListField(child=serializers.CharField())
    objectives = serializers.ListField(child=serializers.CharField())
    logo = serializers.URLField()
    language = serializers.CharField()

class DepartmentResponseSerializer(serializers.Serializer):
    """Serializer for department information response"""

    success = serializers.BooleanField()
    message = serializers.CharField()
    department = DepartmentInfoSerializer(allow_null=True)

