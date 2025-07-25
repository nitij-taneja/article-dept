import requests
from typing import List, Dict, Any
from urllib.parse import quote
import json
import time
from duckduckgo_search import DDGS

class ArticleSearchService:
    """Service for searching articles across different sources"""
    
    def __init__(self):
        self.ddgs = DDGS()
    
    def search_articles(self, query: str, language: str = 'en', max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for articles based on query and language
        
        Args:
            query: Search query
            language: Language code ('en' or 'ar')
            max_results: Maximum number of results to return
            
        Returns:
            List of article dictionaries with title, url, snippet
        """
        try:
            results = []
            
            # Use DuckDuckGo search
            ddg_results = self._search_duckduckgo_real(query, language, max_results)
            results.extend(ddg_results)
            
            # Remove duplicates and limit results
            unique_results = self._remove_duplicates(results)
            return unique_results[:max_results]
            
        except Exception as e:
            print(f"Error in search_articles: {str(e)}")
            return []
    
    def _search_duckduckgo_real(self, query: str, language: str, max_results: int) -> List[Dict[str, Any]]:
        """Real DuckDuckGo search using duckduckgo-search package"""
        try:
            # Modify query for Arabic content if needed
            if language == 'ar':
                # Add Arabic language hints to the query
                search_query = f"{query} lang:ar OR site:arabic OR الـ"
            else:
                search_query = query
            
            # Perform search using DuckDuckGo
            search_results = []
            
            # Use text search
            with self.ddgs as ddgs:
                results = ddgs.text(
                    keywords=search_query,
                    region='wt-wt',  # Worldwide
                    safesearch='moderate',
                    timelimit=None,
                    max_results=max_results * 2  # Get more results to filter
                )
                
                for result in results:
                    if len(search_results) >= max_results:
                        break
                        
                    # Filter for article-like content
                    title = result.get('title', '')
                    url = result.get('href', '')
                    snippet = result.get('body', '')
                    
                    # Basic filtering for article content
                    if self._is_article_like(title, url, snippet):
                        search_results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'source': 'duckduckgo'
                        })
            
            return search_results
            
        except Exception as e:
            print(f"Error in DuckDuckGo search: {str(e)}")
            # Fallback to mock data if search fails
            return self._get_fallback_results(query, language, max_results)
    
    def _is_article_like(self, title: str, url: str, snippet: str) -> bool:
        """Check if the result looks like an article"""
        # Filter out non-article content
        exclude_domains = ['youtube.com', 'twitter.com', 'facebook.com', 'instagram.com', 'reddit.com']
        exclude_keywords = ['video', 'watch', 'download', 'buy', 'shop', 'price']
        
        # Check URL
        for domain in exclude_domains:
            if domain in url.lower():
                return False
        
        # Check title and snippet for article indicators
        article_indicators = ['article', 'news', 'report', 'analysis', 'study', 'research', 'guide']
        content = (title + ' ' + snippet).lower()
        
        # Must have reasonable length
        if len(title) < 10 or len(snippet) < 50:
            return False
        
        # Exclude if contains too many exclude keywords
        exclude_count = sum(1 for keyword in exclude_keywords if keyword in content)
        if exclude_count > 1:
            return False
        
        return True
    
    def _get_fallback_results(self, query: str, language: str, max_results: int) -> List[Dict[str, Any]]:
        """Fallback mock results if real search fails"""
        if language == 'ar':
            return [
                {
                    'title': f"مقال حول {query} - مثال 1",
                    'url': f"https://example.com/ar/article1?q={quote(query)}",
                    'snippet': f"هذا مقال تجريبي حول {query}. يحتوي على معلومات ورؤى ذات صلة.",
                    'source': 'fallback'
                },
                {
                    'title': f"بحث في {query} - مثال 2", 
                    'url': f"https://example.com/ar/article2?q={quote(query)}",
                    'snippet': f"بحث وتحليل شامل حول موضوع {query}.",
                    'source': 'fallback'
                }
            ]
        else:
            return [
                {
                    'title': f"Article about {query} - Example 1",
                    'url': f"https://example.com/article1?q={quote(query)}",
                    'snippet': f"This is a sample article about {query}. It contains relevant information and insights.",
                    'source': 'fallback'
                },
                {
                    'title': f"Research on {query} - Example 2", 
                    'url': f"https://example.com/article2?q={quote(query)}",
                    'snippet': f"Comprehensive research and analysis on {query} topic.",
                    'source': 'fallback'
                }
            ]
    
    def _remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on URL"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results

class NewsAPISearchService:
    """Alternative search service using news APIs"""
    
    def __init__(self):
        # You can add NewsAPI or other news API keys here
        self.news_sources = {
            'newsapi': None,  # Requires API key
            'rss_feeds': [
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.bbci.co.uk/news/rss.xml',
                'https://www.aljazeera.com/xml/rss/all.xml'  # Arabic content
            ]
        }
    
    def search_news_articles(self, query: str, language: str = 'en') -> List[Dict[str, Any]]:
        """Search for news articles"""
        # Implementation for news-specific search
        # This would integrate with news APIs or RSS feeds
        return []

