# Article Search API with Groq LLM Integration

A Django-based REST API that provides intelligent article search and content retrieval with multi-language support (English and Arabic) and AI-powered content processing using Groq LLM.

## Features

- **Article Search**: Search for articles across the web with language-specific filtering
- **Content Extraction**: Retrieve full article content from URLs
- **AI Summarization**: Generate intelligent summaries using Groq LLM
- **Keyword Extraction**: Extract relevant keywords using AI
- **Multi-language Support**: English and Arabic language support
- **Real-time Search**: Uses DuckDuckGo search for real-time results

## API Endpoints

### 1. Article Search API

**Endpoint**: `POST /api/search/`

Search for articles by title with language options.

**Request Body**:
```json
{
    "query": "artificial intelligence",
    "language": "en",
    "max_results": 5
}
```

**Parameters**:
- `query` (string, required): Search query for articles
- `language` (string, optional): Language for search results ("en" or "ar", default: "en")
- `max_results` (integer, optional): Maximum number of results (1-10, default: 5)

**Response**:
```json
{
    "success": true,
    "message": "Found 3 articles",
    "results": [
        {
            "id": "e407e244-4b49-4760-a156-80e40d94f0b8",
            "title": "Artificial intelligence - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "snippet": "Artificial intelligence (AI) is the capability of computational systems...",
            "language": "en",
            "search_query": "artificial intelligence",
            "created_at": "2025-07-25T09:08:58.189210Z"
        }
    ],
    "total_count": 3
}
```

### 2. Article Content Retrieval API

**Endpoint**: `POST /api/content/`

Retrieve full article content by ID with AI-powered processing.

**Request Body**:
```json
{
    "article_id": "e407e244-4b49-4760-a156-80e40d94f0b8",
    "include_summary": true
}
```

**Parameters**:
- `article_id` (UUID, required): Article ID from search results
- `include_summary` (boolean, optional): Include AI-generated summary (default: true)

**Response**:
```json
{
    "success": true,
    "message": "Content retrieved successfully",
    "content": {
        "search_result": {
            "id": "e407e244-4b49-4760-a156-80e40d94f0b8",
            "title": "Artificial intelligence - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "snippet": "Artificial intelligence (AI) is the capability...",
            "language": "en",
            "search_query": "artificial intelligence",
            "created_at": "2025-07-25T09:08:58.189210Z"
        },
        "full_text": "Full article content here...",
        "summary": "AI-generated summary of the article...",
        "author": "Author Name",
        "publish_date": "2025-07-25T00:00:00Z",
        "keywords": ["artificial intelligence", "machine learning", "AI"],
        "fetched_at": "2025-07-25T09:09:24.235751Z"
    }
}
```

### 3. Health Check API

**Endpoint**: `GET /api/health/`

Check API health status.

**Response**:
```json
{
    "status": "healthy",
    "message": "Article Search API is running",
    "version": "1.0.0"
}
```

## Installation and Setup

### Prerequisites

- Python 3.11+
- Django 5.2+
- Groq API Key

### Installation Steps

1. **Clone the repository**:
```bash
git clone <repository-url>
cd groq_article_api
```

2. **Install dependencies**:
```bash
pip install django djangorestframework django-cors-headers groq newspaper3k python-decouple duckduckgo-search lxml[html_clean]
```

3. **Set up environment variables**:
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
SECRET_KEY=your-secret-key-here
```

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Start the development server**:
```bash
python manage.py runserver 0.0.0.0:8000
```

## Usage Examples

### Example 1: Search for English Articles

```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "language": "en",
    "max_results": 3
  }'
```

### Example 2: Search for Arabic Articles

```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "الذكاء الاصطناعي",
    "language": "ar",
    "max_results": 5
  }'
```

### Example 3: Retrieve Article Content

```bash
curl -X POST http://localhost:8000/api/content/ \
  -H "Content-Type: application/json" \
  -d '{
    "article_id": "your-article-id-here",
    "include_summary": true
  }'
```

## Architecture

### Components

1. **Django REST Framework**: API framework
2. **DuckDuckGo Search**: Web search functionality
3. **Newspaper3k**: Article content extraction
4. **Groq LLM**: AI-powered content processing
5. **SQLite**: Database for storing search results and content

### Models

- **ArticleSearchResult**: Stores search results with metadata
- **ArticleContent**: Stores extracted article content and AI-generated summaries

### Services

- **ArticleSearchService**: Handles web search functionality
- **GroqLLMService**: Manages AI operations (summarization, keyword extraction)

## AI Features

### Groq LLM Integration

The API uses Groq's LLM for several AI-powered features:

1. **Content Summarization**: Generates concise summaries of articles
2. **Keyword Extraction**: Identifies important keywords from content
3. **Sentiment Analysis**: Analyzes the sentiment of article content
4. **Translation**: Supports content translation between languages

### Language Support

- **English**: Full support for search and content processing
- **Arabic**: Search support with Arabic query handling and content processing

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Article not found
- **500 Internal Server Error**: Server-side errors

Example error response:
```json
{
    "success": false,
    "message": "Invalid request parameters",
    "errors": {
        "query": ["This field is required."]
    }
}
```

## Rate Limiting and Performance

- **Search Results**: Cached to improve performance
- **Content Extraction**: Cached to avoid re-fetching
- **AI Processing**: Optimized for speed and accuracy

## Security

- **CORS**: Configured for cross-origin requests
- **Environment Variables**: Sensitive data stored securely
- **Input Validation**: All inputs validated and sanitized

## Deployment

For production deployment:

1. Set `DEBUG=False` in environment variables
2. Configure a production database (PostgreSQL recommended)
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Set up proper logging and monitoring
5. Configure SSL/HTTPS

## API Testing

Test the API using the provided examples or tools like Postman, curl, or any HTTP client.

## Support

For issues or questions, please refer to the documentation or contact the development team.

## License

This project is licensed under the MIT License.

