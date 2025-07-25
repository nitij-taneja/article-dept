from groq import Groq
from django.conf import settings
import json
import uuid
import requests
import re
from urllib.parse import quote_plus
from typing import Optional, Dict, Any, List

class GroqLLMService:
    """Service for Groq LLM operations including summarization and translation"""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama3-8b-8192"  # Default Groq model
    
    def summarize_article(self, text: str, language: str = 'en', max_length: int = 200) -> Optional[str]:
        """
        Generate a summary of the article text using Groq LLM
        
        Args:
            text: Article text to summarize
            language: Target language for summary ('en' or 'ar')
            max_length: Maximum length of summary in words
            
        Returns:
            Generated summary or None if failed
        """
        try:
            if not text or len(text.strip()) < 50:
                return "Text too short to summarize"
            
            # Prepare prompt based on language
            if language == 'ar':
                prompt = f"""
                قم بتلخيص المقال التالي باللغة العربية في حوالي {max_length} كلمة. 
                اجعل الملخص واضحاً ومفيداً ويغطي النقاط الرئيسية:

                {text[:4000]}  # Limit text to avoid token limits
                
                الملخص:
                """
            else:
                prompt = f"""
                Please summarize the following article in approximately {max_length} words. 
                Make the summary clear, informative, and cover the main points:

                {text[:4000]}  # Limit text to avoid token limits
                
                Summary:
                """
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"Error in summarize_article: {str(e)}")
            return None
    
    def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language ('en' or 'ar')
            
        Returns:
            Translated text or None if failed
        """
        try:
            if target_language == 'ar':
                prompt = f"""
                ترجم النص التالي إلى اللغة العربية بدقة مع الحفاظ على المعنى الأصلي:

                {text[:3000]}
                
                الترجمة:
                """
            else:
                prompt = f"""
                Translate the following text to English accurately while preserving the original meaning:

                {text[:3000]}
                
                Translation:
                """
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=1000,
                temperature=0.2
            )
            
            translation = response.choices[0].message.content.strip()
            return translation
            
        except Exception as e:
            print(f"Error in translate_text: {str(e)}")
            return None
    
    def extract_keywords(self, text: str, language: str = 'en', max_keywords: int = 10) -> list:
        """
        Extract keywords from text using Groq LLM
        
        Args:
            text: Text to extract keywords from
            language: Language of the text
            max_keywords: Maximum number of keywords to extract
            
        Returns:
            List of keywords
        """
        try:
            if language == 'ar':
                prompt = f"""
                استخرج أهم {max_keywords} كلمات مفتاحية من النص التالي. 
                أرجع الكلمات المفتاحية كقائمة مفصولة بفواصل:

                {text[:2000]}
                
                الكلمات المفتاحية:
                """
            else:
                prompt = f"""
                Extract the top {max_keywords} most important keywords from the following text. 
                Return the keywords as a comma-separated list:

                {text[:2000]}
                
                Keywords:
                """
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=200,
                temperature=0.3
            )
            
            keywords_text = response.choices[0].message.content.strip()
            # Parse keywords from response
            keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
            return keywords[:max_keywords]
            
        except Exception as e:
            print(f"Error in extract_keywords: {str(e)}")
            return []
    
    def analyze_sentiment(self, text: str, language: str = 'en') -> Dict[str, Any]:
        """
        Analyze sentiment of the text
        
        Args:
            text: Text to analyze
            language: Language of the text
            
        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            if language == 'ar':
                prompt = f"""
                حلل المشاعر في النص التالي وأرجع النتيجة بالتنسيق التالي:
                المشاعر: [إيجابي/سلبي/محايد]
                الثقة: [رقم من 0 إلى 1]
                التفسير: [تفسير قصير]

                النص:
                {text[:1500]}
                """
            else:
                prompt = f"""
                Analyze the sentiment of the following text and return the result in this format:
                Sentiment: [positive/negative/neutral]
                Confidence: [number from 0 to 1]
                Explanation: [brief explanation]

                Text:
                {text[:1500]}
                """
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=300,
                temperature=0.2
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse the response (basic parsing)
            sentiment = "neutral"
            confidence = 0.5
            explanation = result_text
            
            if "positive" in result_text.lower() or "إيجابي" in result_text:
                sentiment = "positive"
            elif "negative" in result_text.lower() or "سلبي" in result_text:
                sentiment = "negative"
            
            return {
                "sentiment": sentiment,
                "confidence": confidence,
                "explanation": explanation
            }
            
        except Exception as e:
            print(f"Error in analyze_sentiment: {str(e)}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "explanation": f"Analysis failed: {str(e)}"
            }

    def generate_article_search_results(self, query: str, language: str = 'en', max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Generate comprehensive article search results using LLM

        Args:
            query: Search query
            language: Target language ('en' or 'ar')
            max_results: Maximum number of results to generate

        Returns:
            List of generated article results with detailed content
        """
        try:
            if language == 'ar':
                prompt = f"""
                أنشئ {max_results} مقالات تفصيلية حول موضوع "{query}". لكل مقال، قدم:

                1. العنوان (جذاب ومناسب)
                2. ملخص طويل (أكثر من 200 كلمة)
                3. الفئة مع: الاسم، وصف مفصل (أكثر من 200 كلمة)، رابط ويكيبيديا، صورة وهمية
                4. المؤلف مع: الاسم، المهنة، وصف مفصل، رابط ويكيبيديا، صورة وهمية
                5. المحتوى الكامل للمقال (أكثر من 500 كلمة)
                6. ملخص شامل (200-300 كلمة)

                أرجع النتيجة بتنسيق JSON صالح:
                """
            else:
                prompt = f"""
                Generate {max_results} detailed articles about "{query}". For each article, provide:

                1. Title (engaging and relevant)
                2. Long snippet (more than 200 words)
                3. Category with: name, detailed description (200+ words), wikipedia link, image URL
                4. Author with: name, profession, detailed description, wikipedia link, image URL
                5. Full article content (500+ words)
                6. Comprehensive summary (200-300 words)

                Return the result in valid JSON format:
                [
                  {{
                    "id": "unique-uuid",
                    "title": "Article Title",
                    "snippet": "Long detailed snippet...",
                    "category": {{
                      "name": "Category Name",
                      "description": "Detailed category description...",
                      "wikipedia_link": "https://en.wikipedia.org/wiki/Category_Name",
                      "image": "https://example.com/category-image.jpg"
                    }},
                    "author": {{
                      "name": "Author Name",
                      "profession": "writer/journalist/researcher/etc",
                      "description": "Detailed author bio...",
                      "wikipedia_link": "https://en.wikipedia.org/wiki/Author_Name",
                      "image": "https://example.com/author-image.jpg"
                    }},
                    "content": "Full article content...",
                    "summary": "Comprehensive summary..."
                  }}
                ]
                """

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=4000,
                temperature=0.7
            )

            result_text = response.choices[0].message.content.strip()

            # Try to parse JSON response
            try:
                articles = json.loads(result_text)
                if not isinstance(articles, list):
                    articles = [articles]

                # Ensure each article has a unique ID and real images
                for article in articles:
                    if 'id' not in article:
                        article['id'] = str(uuid.uuid4())

                    # Get real images for category and author
                    if 'category' in article and isinstance(article['category'], dict):
                        category_name = article['category'].get('name', query)
                        article['category']['image'] = self.search_for_reliable_image(category_name, "category")

                    if 'author' in article and isinstance(article['author'], dict):
                        author_name = article['author'].get('name', 'professional author')
                        article['author']['image'] = self.search_for_reliable_image(f"{author_name} portrait", "person")

                return articles[:max_results]

            except json.JSONDecodeError:
                # Fallback: create structured articles from text response
                return self._create_fallback_articles(query, language, max_results, result_text)

        except Exception as e:
            print(f"Error in generate_article_search_results: {str(e)}")
            return self._create_fallback_articles(query, language, max_results)

    def _create_fallback_articles(self, query: str, language: str, max_results: int, content: str = None) -> List[Dict[str, Any]]:
        """Create fallback articles when LLM generation fails"""
        articles = []

        for i in range(max_results):
            if language == 'ar':
                article = {
                    "id": str(uuid.uuid4()),
                    "title": f"مقال شامل حول {query} - الجزء {i+1}",
                    "snippet": f"هذا مقال تفصيلي يتناول موضوع {query} من زوايا متعددة. يقدم المقال تحليلاً عميقاً للموضوع مع استعراض الجوانب المختلفة والتطورات الحديثة. يهدف هذا المحتوى إلى تقديم فهم شامل للقارئ حول {query} وتأثيراته على المجتمع والاقتصاد. كما يستكشف المقال التحديات والفرص المرتبطة بهذا الموضوع، ويقدم رؤى من خبراء مختصين في المجال. المقال مدعوم بأمثلة عملية ودراسات حالة توضح التطبيقات الواقعية للموضوع.",
                    "category": {
                        "name": "تكنولوجيا ومعلومات",
                        "description": "فئة شاملة تغطي أحدث التطورات في مجال التكنولوجيا والمعلومات. تشمل هذه الفئة مواضيع متنوعة مثل الذكاء الاصطناعي، والحوسبة السحابية، وأمن المعلومات، والتطبيقات الذكية. تهدف إلى تقديم محتوى عالي الجودة يساعد القراء على فهم التقنيات الحديثة وتأثيرها على حياتنا اليومية. كما تتناول التحديات والفرص في عالم التكنولوجيا المتطور.",
                        "wikipedia_link": "https://ar.wikipedia.org/wiki/تكنولوجيا_المعلومات",
                        "image": self.search_for_reliable_image("تكنولوجيا المعلومات", "category")
                    },
                    "author": {
                        "name": f"د. أحمد محمد الخبير {i+1}",
                        "profession": "كاتب وباحث في التكنولوجيا",
                        "description": "خبير متخصص في مجال التكنولوجيا والابتكار مع خبرة تزيد عن 15 عاماً في البحث والكتابة. حاصل على درجة الدكتوراه في علوم الحاسوب ومؤلف لعدة كتب في مجال التكنولوجيا. يعمل كمستشار تقني لعدة شركات ومؤسسات، ويساهم بانتظام في المؤتمرات العلمية والمجلات المتخصصة.",
                        "wikipedia_link": f"https://ar.wikipedia.org/wiki/أحمد_محمد_الخبير_{i+1}",
                        "image": self.search_for_reliable_image(f"د. أحمد محمد الخبير {i+1}", "person")
                    },
                    "content": content or f"محتوى مفصل حول {query}...",
                    "summary": f"ملخص شامل للمقال حول {query} يغطي النقاط الرئيسية والاستنتاجات المهمة."
                }
            else:
                article = {
                    "id": str(uuid.uuid4()),
                    "title": f"Comprehensive Article on {query} - Part {i+1}",
                    "snippet": f"This detailed article explores the topic of {query} from multiple perspectives. It provides in-depth analysis of the subject matter, covering various aspects and recent developments. The content aims to give readers a comprehensive understanding of {query} and its implications for society and economy. The article also examines challenges and opportunities related to this topic, offering insights from field experts. It is supported by practical examples and case studies that illustrate real-world applications of the subject matter. The piece is designed to be both informative and accessible to readers with varying levels of expertise.",
                    "category": {
                        "name": "Technology & Innovation",
                        "description": "A comprehensive category covering the latest developments in technology and innovation. This category encompasses diverse topics including artificial intelligence, cloud computing, cybersecurity, and smart applications. It aims to provide high-quality content that helps readers understand modern technologies and their impact on our daily lives. The category also addresses challenges and opportunities in the evolving world of technology, featuring expert analysis and forward-looking perspectives on technological trends.",
                        "wikipedia_link": "https://en.wikipedia.org/wiki/Technology",
                        "image": self.search_for_reliable_image("Technology Innovation", "category")
                    },
                    "author": {
                        "name": f"Dr. Sarah Johnson Expert {i+1}",
                        "profession": "technology writer and researcher",
                        "description": "A specialized expert in technology and innovation with over 15 years of experience in research and writing. Holds a Ph.D. in Computer Science and is the author of several books on technology. Works as a technical consultant for various companies and institutions, regularly contributing to scientific conferences and specialized journals. Known for making complex technological concepts accessible to general audiences.",
                        "wikipedia_link": f"https://en.wikipedia.org/wiki/Sarah_Johnson_Expert_{i+1}",
                        "image": self.search_for_reliable_image(f"Dr. Sarah Johnson Expert {i+1}", "person")
                    },
                    "content": content or f"Detailed content about {query}...",
                    "summary": f"Comprehensive summary of the article on {query} covering key points and important conclusions."
                }

            articles.append(article)

        return articles

    def search_for_reliable_image(self, query: str, image_type: str = "general") -> str:
        """
        Main function to search for reliable images.
        First tries Google Images, then falls back to curated images.
        """
        # Try Google Images first
        google_result = self.search_google_images(query, image_type)

        # If Google search returned a valid result, use it
        if google_result and not google_result.startswith('https://placehold.co') and not google_result.startswith('https://cdn.britannica.com'):
            return google_result

        # Otherwise use the fallback (which includes Britannica images)
        return google_result

    def search_google_images(self, query: str, image_type: str = "general") -> str:
        """
        Search Google Images for free using web scraping (no API key required).
        Returns the first valid image URL found.
        """
        try:
            # Prepare search query
            search_query = f"{query} {image_type}" if image_type != "general" else query
            encoded_query = quote_plus(search_query)

            # Google Images search URL
            search_url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&safe=active"

            # Headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Make request to Google Images
            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200:
                # Extract image URLs from the response
                image_pattern = r'"(https?://[^"]*\.(?:jpg|jpeg|png|webp|gif))"'
                matches = re.findall(image_pattern, response.text, re.IGNORECASE)

                # Filter out unwanted domains and find a good image
                for url in matches:
                    if self.is_valid_google_image_url(url):
                        return url

            # If Google search fails, fall back to curated images
            return self.get_fallback_image(query, image_type)

        except Exception as e:
            print(f"Error in Google Images search: {str(e)}")
            return self.get_fallback_image(query, image_type)

    def is_valid_google_image_url(self, url: str) -> bool:
        """
        Validate if a Google Images URL is suitable for use.
        """
        if not url or not isinstance(url, str):
            return False

        url_lower = url.lower()

        # Reject unwanted domains
        blocked_domains = [
            'wikimedia.org',
            'wikipedia.org',
            'google.com',
            'googleusercontent.com',
            'gstatic.com',
            'encrypted-tbn',  # Google's encrypted thumbnails
        ]

        if any(domain in url_lower for domain in blocked_domains):
            return False

        # Must be a direct image URL
        if not url_lower.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            return False

        return True

    def get_fallback_image(self, query: str, image_type: str = "general") -> str:
        """
        Get fallback images when Google search fails.
        Uses curated high-quality image sources.
        """
        try:
            # Try Britannica images for educational content
            if image_type in ["category", "educational", "general"]:
                britannica_url = self.search_britannica_images(query)
                if britannica_url:
                    return britannica_url

            # Try Unsplash for high-quality stock photos
            unsplash_url = self.search_unsplash_images(query, image_type)
            if unsplash_url:
                return unsplash_url

            # Final fallback to placeholder
            return f"https://placehold.co/400x300/2563eb/ffffff?text={quote_plus(query[:20])}"

        except Exception as e:
            print(f"Error in fallback image search: {str(e)}")
            return f"https://placehold.co/400x300/2563eb/ffffff?text={quote_plus(query[:20])}"

    def search_britannica_images(self, query: str) -> Optional[str]:
        """
        Search Britannica for educational images.
        """
        try:
            search_url = f"https://www.britannica.com/search?query={quote_plus(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(search_url, headers=headers, timeout=8)
            if response.status_code == 200:
                # Look for Britannica image URLs
                image_pattern = r'(https://cdn\.britannica\.com/[^"]*\.(?:jpg|jpeg|png))'
                matches = re.findall(image_pattern, response.text, re.IGNORECASE)

                if matches:
                    return matches[0]

            return None

        except Exception as e:
            print(f"Error searching Britannica: {str(e)}")
            return None

    def search_unsplash_images(self, query: str, image_type: str) -> Optional[str]:
        """
        Search Unsplash for high-quality stock photos.
        """
        try:
            # Unsplash Source API (free, no key required)
            # Categories: nature, city, technology, food, abstract, etc.
            category_map = {
                "technology": "technology",
                "nature": "nature",
                "science": "technology",
                "business": "business",
                "education": "education",
                "general": "abstract"
            }

            category = category_map.get(image_type, "abstract")
            unsplash_url = f"https://source.unsplash.com/800x600/?{category},{quote_plus(query)}"

            # Test if the URL is accessible
            response = requests.head(unsplash_url, timeout=5)
            if response.status_code == 200:
                return unsplash_url

            return None

        except Exception as e:
            print(f"Error searching Unsplash: {str(e)}")
            return None

    def generate_department_info(self, department_input: str, language: str = 'en') -> Dict[str, Any]:
        """
        Generate comprehensive department information using LLM

        Args:
            department_input: Department name or code (e.g., "IT", "Finance", "HR")
            language: Target language ('en' or 'ar')

        Returns:
            Dictionary with department name, code, description, and logo
        """
        try:
            if language == 'ar':
                prompt = f"""
                أنشئ معلومات شاملة عن القسم "{department_input}". يجب أن تتضمن:

                1. الاسم الكامل للقسم باللغة العربية
                2. الرمز أو الاختصار (مثل IT, HR, FIN)
                3. وصف مفصل للقسم (200+ كلمة)
                4. المسؤوليات الرئيسية
                5. الأهداف والمهام
                6. رابط شعار مناسب للقسم

                أرجع النتيجة بتنسيق JSON صالح:
                {{
                  "name": "الاسم الكامل للقسم",
                  "code": "الرمز",
                  "description": "وصف مفصل...",
                  "responsibilities": ["مسؤولية 1", "مسؤولية 2", ...],
                  "objectives": ["هدف 1", "هدف 2", ...],
                  "logo": "رابط الشعار",
                  "language": "ar"
                }}
                """
            else:
                prompt = f"""
                Generate comprehensive information about the department "{department_input}". Include:

                1. Full department name in English
                2. Department code/abbreviation (e.g., IT, HR, FIN)
                3. Detailed description (200+ words)
                4. Key responsibilities
                5. Objectives and goals
                6. Appropriate logo URL

                Return as valid JSON:
                {{
                  "name": "Full Department Name",
                  "code": "DEPT_CODE",
                  "description": "Detailed description...",
                  "responsibilities": ["responsibility 1", "responsibility 2", ...],
                  "objectives": ["objective 1", "objective 2", ...],
                  "logo": "logo_url",
                  "language": "en"
                }}
                """

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=2000,
                temperature=0.5
            )

            result_text = response.choices[0].message.content.strip()

            # Try to parse JSON response
            try:
                dept_data = json.loads(result_text)

                # Get a real logo for the department
                dept_name = dept_data.get('name', department_input)
                dept_code = dept_data.get('code', department_input)

                # Search for department-specific logo
                logo_url = self.search_department_logo(dept_name, dept_code, language)
                dept_data['logo'] = logo_url

                return dept_data

            except json.JSONDecodeError:
                # Fallback: create structured department info
                return self._create_fallback_department(department_input, language, result_text)

        except Exception as e:
            print(f"Error in generate_department_info: {str(e)}")
            return self._create_fallback_department(department_input, language)

    def search_department_logo(self, dept_name: str, dept_code: str, language: str) -> str:
        """
        Search for department-specific logos
        """
        try:
            # Create search queries for department logos
            search_queries = [
                f"{dept_name} department logo",
                f"{dept_code} department icon",
                f"{dept_name} corporate logo",
                f"department {dept_code} symbol"
            ]

            # Try each search query
            for query in search_queries:
                try:
                    logo_url = self.search_for_reliable_image(query, "logo")
                    if logo_url and not logo_url.startswith('https://placehold.co'):
                        return logo_url
                except:
                    continue

            # Fallback to icon-based search
            return self.get_department_icon_fallback(dept_name, dept_code)

        except Exception as e:
            print(f"Error searching department logo: {str(e)}")
            return self.get_department_icon_fallback(dept_name, dept_code)

    def get_department_icon_fallback(self, dept_name: str, dept_code: str) -> str:
        """
        Get fallback department icons/logos
        """
        try:
            # Map common departments to icon categories
            dept_icon_map = {
                'IT': 'technology computer server',
                'HR': 'human resources people team',
                'FINANCE': 'finance money accounting calculator',
                'MARKETING': 'marketing advertising megaphone',
                'SALES': 'sales business handshake',
                'OPERATIONS': 'operations management gear',
                'LEGAL': 'legal law justice scales',
                'ADMIN': 'administration office building',
                'RESEARCH': 'research science laboratory microscope',
                'DEVELOPMENT': 'development engineering tools',
                'SUPPORT': 'customer support service headset',
                'SECURITY': 'security shield protection lock'
            }

            # Normalize department code
            normalized_code = dept_code.upper().replace(' ', '_')

            # Find matching icon category
            icon_category = None
            for key, category in dept_icon_map.items():
                if key in normalized_code or key.lower() in dept_name.lower():
                    icon_category = category
                    break

            # If no specific match, use generic department icon
            if not icon_category:
                icon_category = "department office building corporate"

            # Search for icon
            icon_url = self.search_for_reliable_image(icon_category, "icon")

            # Final fallback to a generic department placeholder
            if not icon_url or icon_url.startswith('https://placehold.co'):
                return f"https://placehold.co/200x200/3b82f6/ffffff?text={quote_plus(dept_code[:3])}"

            return icon_url

        except Exception as e:
            print(f"Error in department icon fallback: {str(e)}")
            return f"https://placehold.co/200x200/3b82f6/ffffff?text={quote_plus(dept_code[:3])}"

    def _create_fallback_department(self, department_input: str, language: str, content_text: str = None) -> Dict[str, Any]:
        """
        Create fallback department info when LLM generation fails
        """
        try:
            # Determine department code and name
            dept_code = self._extract_department_code(department_input)
            dept_name = self._extract_department_name(department_input, language)

            # Get logo
            logo_url = self.get_department_icon_fallback(dept_name, dept_code)

            if language == 'ar':
                return {
                    "name": dept_name,
                    "code": dept_code,
                    "description": f"قسم {dept_name} هو أحد الأقسام المهمة في المؤسسة، يتولى مسؤوليات متعددة ومتنوعة تساهم في تحقيق أهداف المنظمة. يعمل هذا القسم على تطوير وتنفيذ الاستراتيجيات والسياسات المتعلقة بمجال تخصصه، ويضم فريقاً من المختصين والخبراء ذوي الكفاءة العالية. يسعى القسم إلى تحقيق التميز في الأداء وتقديم أفضل الخدمات للعملاء الداخليين والخارجيين، مع الحرص على مواكبة أحدث التطورات والتقنيات في مجال عمله.",
                    "responsibilities": [
                        f"إدارة وتنسيق أنشطة {dept_name}",
                        "تطوير السياسات والإجراءات",
                        "ضمان الجودة والامتثال للمعايير",
                        "التدريب وتطوير الموظفين",
                        "إعداد التقارير والتحليلات"
                    ],
                    "objectives": [
                        "تحقيق الأهداف الاستراتيجية للمؤسسة",
                        "تحسين الكفاءة والإنتاجية",
                        "ضمان رضا العملاء",
                        "التطوير المستمر للعمليات",
                        "الابتكار والتميز في الأداء"
                    ],
                    "logo": logo_url,
                    "language": "ar"
                }
            else:
                return {
                    "name": dept_name,
                    "code": dept_code,
                    "description": f"The {dept_name} department is a vital component of the organization, responsible for multiple and diverse functions that contribute to achieving organizational goals. This department develops and implements strategies and policies related to its area of expertise, comprising a team of qualified specialists and experts with high competency. The department strives to achieve excellence in performance and deliver the best services to internal and external customers, while keeping pace with the latest developments and technologies in its field of work. It plays a crucial role in organizational success through effective management, strategic planning, and continuous improvement initiatives.",
                    "responsibilities": [
                        f"Managing and coordinating {dept_name} activities",
                        "Developing policies and procedures",
                        "Ensuring quality and compliance with standards",
                        "Training and staff development",
                        "Preparing reports and analyses"
                    ],
                    "objectives": [
                        "Achieve organizational strategic goals",
                        "Improve efficiency and productivity",
                        "Ensure customer satisfaction",
                        "Continuous process improvement",
                        "Innovation and performance excellence"
                    ],
                    "logo": logo_url,
                    "language": "en"
                }

        except Exception as e:
            print(f"Error creating fallback department: {str(e)}")
            return {
                "name": department_input,
                "code": department_input.upper()[:3],
                "description": f"Department information for {department_input}",
                "responsibilities": ["General department responsibilities"],
                "objectives": ["General department objectives"],
                "logo": f"https://placehold.co/200x200/3b82f6/ffffff?text={quote_plus(department_input[:3])}",
                "language": language
            }

    def _extract_department_code(self, department_input: str) -> str:
        """Extract or generate department code"""
        # Common department mappings
        dept_mappings = {
            'information technology': 'IT',
            'human resources': 'HR',
            'finance': 'FIN',
            'marketing': 'MKT',
            'sales': 'SAL',
            'operations': 'OPS',
            'legal': 'LEG',
            'administration': 'ADM',
            'research': 'R&D',
            'development': 'DEV',
            'support': 'SUP',
            'security': 'SEC'
        }

        input_lower = department_input.lower()

        # Check for exact matches
        for key, code in dept_mappings.items():
            if key in input_lower:
                return code

        # If already looks like a code, return as is
        if len(department_input) <= 4 and department_input.isupper():
            return department_input

        # Generate code from first letters
        words = department_input.split()
        if len(words) > 1:
            return ''.join(word[0].upper() for word in words[:3])
        else:
            return department_input[:3].upper()

    def _extract_department_name(self, department_input: str, language: str) -> str:
        """Extract or generate full department name"""
        # Common department full names
        if language == 'ar':
            dept_names = {
                'IT': 'تكنولوجيا المعلومات',
                'HR': 'الموارد البشرية',
                'FIN': 'المالية',
                'MKT': 'التسويق',
                'SAL': 'المبيعات',
                'OPS': 'العمليات',
                'LEG': 'الشؤون القانونية',
                'ADM': 'الإدارة',
                'R&D': 'البحث والتطوير',
                'DEV': 'التطوير',
                'SUP': 'الدعم',
                'SEC': 'الأمن'
            }
        else:
            dept_names = {
                'IT': 'Information Technology',
                'HR': 'Human Resources',
                'FIN': 'Finance',
                'MKT': 'Marketing',
                'SAL': 'Sales',
                'OPS': 'Operations',
                'LEG': 'Legal Affairs',
                'ADM': 'Administration',
                'R&D': 'Research and Development',
                'DEV': 'Development',
                'SUP': 'Support',
                'SEC': 'Security'
            }

        # Check if input is a code
        input_upper = department_input.upper()
        if input_upper in dept_names:
            return dept_names[input_upper]

        # If already a full name, return as is (with proper capitalization)
        return department_input.title()

