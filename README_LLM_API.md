# LLM-Based Article Search API

## Overview

This is a comprehensive article search API that uses **Large Language Models (LLM)** via Groq to generate detailed article content **without any database operations**. The API generates rich, structured content including categories, authors, and comprehensive summaries.

## Key Features

### ✅ No Database Operations
- Pure LLM-based content generation
- No data persistence or retrieval from databases
- Real-time content generation for each request

### ✅ Rich Content Structure
- **Snippets**: 200+ words for each article
- **Categories**: Name, detailed description (200+ words), Wikipedia links, images
- **Authors**: Name, profession, detailed bio, Wikipedia links, images
- **Full Content**: 500+ words of comprehensive article text
- **Summaries**: 200-300 word comprehensive summaries

### ✅ Multi-language Support
- English (`en`)
- Arabic (`ar`)
- Language-specific content generation

### ✅ Professional Author Profiles
- Various professions: writer, journalist, researcher, collector, etc.
- Detailed biographical information
- Professional credentials and expertise areas

## API Endpoints

### 1. Article Search
**POST** `/api/search/`

Generate comprehensive articles based on search query.

**Request:**
```json
{
    "query": "artificial intelligence",
    "language": "en",
    "max_results": 5
}
```

**Response:**
```json
{
    "success": true,
    "message": "Generated 5 articles",
    "results": [
        {
            "id": "uuid-here",
            "title": "Comprehensive Article Title",
            "snippet": "200+ word detailed snippet...",
            "category": {
                "name": "Technology & Innovation",
                "description": "200+ word category description...",
                "wikipedia_link": "https://en.wikipedia.org/wiki/Technology",
                "image": "https://example.com/tech-category.jpg"
            },
            "author": {
                "name": "Dr. Sarah Johnson",
                "profession": "technology writer and researcher",
                "description": "Detailed author biography...",
                "wikipedia_link": "https://en.wikipedia.org/wiki/Sarah_Johnson",
                "image": "https://example.com/author.jpg"
            },
            "language": "en",
            "search_query": "artificial intelligence"
        }
    ],
    "total_count": 5
}
```

### 2. Article Content
**POST** `/api/content/`

Generate detailed content for a specific article.

**Request:**
```json
{
    "article_id": "uuid-here",
    "query": "artificial intelligence",
    "language": "en",
    "include_summary": true
}
```

**Response:**
```json
{
    "success": true,
    "message": "Content generated successfully",
    "content": {
        "id": "uuid-here",
        "full_text": "800+ word comprehensive article content...",
        "summary": "250-300 word comprehensive summary...",
        "category": {
            "name": "Technology & Innovation",
            "description": "Detailed category description...",
            "wikipedia_link": "https://en.wikipedia.org/wiki/Technology",
            "image": "https://example.com/category.jpg"
        },
        "author": {
            "name": "Dr. Sarah Johnson",
            "profession": "technology writer and researcher",
            "description": "Detailed author biography...",
            "wikipedia_link": "https://en.wikipedia.org/wiki/Sarah_Johnson",
            "image": "https://example.com/author.jpg"
        },
        "keywords": ["artificial intelligence", "technology", "innovation", "machine learning"],
        "publish_date": "2024-01-15"
    }
}
```

### 3. Health Check
**GET** `/api/health/`

Check API status.

**Response:**
```json
{
    "status": "healthy",
    "message": "Article Search API is running",
    "version": "1.0.0"
}
```

## Setup and Installation

### Prerequisites
- Python 3.8+
- Django 5.2+
- Groq API key

### Installation
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export GROQ_API_KEY="your-groq-api-key"
```

3. Run the server:
```bash
python manage.py runserver 8000
```

## Testing

### Run LLM Service Test
```bash
python test_llm_service.py
```

### Run API Integration Test
```bash
python test_llm_api.py
```

## Content Quality Guarantees

### Snippet Requirements
- ✅ Minimum 200 words per snippet
- ✅ Contextually relevant to search query
- ✅ Engaging and informative content

### Category Information
- ✅ Relevant category name
- ✅ 200+ word detailed description
- ✅ Wikipedia links for reference
- ✅ Representative images

### Author Profiles
- ✅ Professional names and credentials
- ✅ Diverse professions (writer, journalist, researcher, collector, etc.)
- ✅ Detailed biographical information
- ✅ Wikipedia links and profile images

### Article Content
- ✅ 500+ words of comprehensive content
- ✅ Well-structured and informative
- ✅ Relevant to the search query
- ✅ Professional writing quality

### Summaries
- ✅ 200-300 word comprehensive summaries
- ✅ Covers key points and conclusions
- ✅ Maintains article context and relevance

## Architecture

### LLM Integration
- **Service**: `GroqLLMService` handles all LLM interactions
- **Model**: Uses `llama3-8b-8192` for content generation
- **Fallback**: Structured fallback content when LLM fails

### No Database Design
- **Stateless**: Each request generates fresh content
- **Scalable**: No database bottlenecks
- **Flexible**: Easy to modify content structure

### Error Handling
- **Graceful Degradation**: Fallback content when LLM fails
- **Structured Responses**: Consistent error messaging
- **Logging**: Comprehensive error tracking

## Example Use Cases

1. **Content Research**: Generate comprehensive articles on any topic
2. **Educational Material**: Create detailed explanations with expert authors
3. **Multi-language Content**: Generate content in English and Arabic
4. **Category Exploration**: Discover related topics and categories
5. **Author Discovery**: Learn about experts in various fields

## Performance Notes

- **Response Time**: 3-10 seconds per request (LLM generation)
- **Concurrency**: Supports multiple simultaneous requests
- **Rate Limiting**: Depends on Groq API limits
- **Caching**: No caching - fresh content every time

## Future Enhancements

- Additional language support
- Custom content templates
- Enhanced author profession categories
- Image generation integration
- Content quality scoring
