from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SearchRequestSerializer, SearchResponseSerializer,
    ContentRequestSerializer, ContentResponseSerializer
)
from .groq_service import GroqLLMService
import uuid

class ArticleSearchView(APIView):
    """
    API endpoint for searching articles using LLM generation

    POST /api/search/
    {
        "query": "artificial intelligence",
        "language": "en",
        "max_results": 5
    }
    """

    def post(self, request):
        """Search for articles based on query and language using LLM"""

        # Validate request data
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request parameters',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        query = validated_data['query']
        language = validated_data['language']
        max_results = validated_data['max_results']

        try:
            # Initialize Groq LLM service
            groq_service = GroqLLMService()

            # Generate comprehensive article results using LLM
            search_results = groq_service.generate_article_search_results(
                query=query,
                language=language,
                max_results=max_results
            )

            # Format results for response (no database operations)
            formatted_results = []
            for result in search_results:
                formatted_result = {
                    'id': result.get('id', str(uuid.uuid4())),
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', ''),
                    'category': result.get('category', {}),
                    'author': result.get('author', {}),
                    'language': language,
                    'search_query': query
                }
                formatted_results.append(formatted_result)

            response_data = {
                'success': True,
                'message': f'Generated {len(formatted_results)} articles',
                'results': formatted_results,
                'total_count': len(formatted_results)
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Search failed: {str(e)}',
                'results': [],
                'total_count': 0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArticleContentView(APIView):
    """
    API endpoint for retrieving article content by ID using LLM generation

    POST /api/content/
    {
        "article_id": "uuid-here",
        "query": "original search query",
        "language": "en",
        "include_summary": true
    }
    """

    def post(self, request):
        """Generate full content for a specific article using LLM"""

        # Validate request data
        serializer = ContentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Invalid request parameters',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        article_id = validated_data['article_id']
        query = validated_data.get('query', 'general topic')
        language = validated_data.get('language', 'en')
        include_summary = validated_data.get('include_summary', True)

        try:
            # Initialize Groq LLM service
            groq_service = GroqLLMService()

            # Generate detailed article content using LLM
            article_content = self._generate_article_content(
                groq_service, article_id, query, language, include_summary
            )

            if article_content:
                return Response({
                    'success': True,
                    'message': 'Content generated successfully',
                    'content': article_content
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to generate article content',
                    'content': None
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Content generation failed: {str(e)}',
                'content': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_article_content(self, groq_service, article_id, query, language, include_summary=True):
        """Generate comprehensive article content using LLM"""
        try:
            if language == 'ar':
                prompt = f"""
                أنشئ مقالاً تفصيلياً شاملاً حول "{query}" بالمعرف {article_id}. يجب أن يتضمن:

                1. المحتوى الكامل (أكثر من 800 كلمة)
                2. الفئة مع: الاسم، وصف مفصل (200+ كلمة)، رابط ويكيبيديا، صورة
                3. المؤلف مع: الاسم، المهنة، وصف مفصل، رابط ويكيبيديا، صورة
                4. الكلمات المفتاحية (10-15 كلمة)
                5. ملخص شامل (250-300 كلمة)
                6. تاريخ النشر

                أرجع النتيجة بتنسيق JSON صالح.
                """
            else:
                prompt = f"""
                Create a comprehensive detailed article about "{query}" with ID {article_id}. Include:

                1. Full article content (800+ words)
                2. Category with: name, detailed description (200+ words), wikipedia link, image
                3. Author with: name, profession, detailed description, wikipedia link, image
                4. Keywords (10-15 keywords)
                5. Comprehensive summary (250-300 words)
                6. Publication date

                Return as valid JSON:
                {{
                  "id": "{article_id}",
                  "full_text": "Complete article content...",
                  "category": {{
                    "name": "Category Name",
                    "description": "Detailed description...",
                    "wikipedia_link": "https://en.wikipedia.org/wiki/...",
                    "image": "https://example.com/image.jpg"
                  }},
                  "author": {{
                    "name": "Author Name",
                    "profession": "profession",
                    "description": "Detailed bio...",
                    "wikipedia_link": "https://en.wikipedia.org/wiki/...",
                    "image": "https://example.com/author.jpg"
                  }},
                  "keywords": ["keyword1", "keyword2", ...],
                  "summary": "Comprehensive summary...",
                  "publish_date": "2024-01-15"
                }}
                """

            response = groq_service.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=groq_service.model,
                max_tokens=4000,
                temperature=0.7
            )

            result_text = response.choices[0].message.content.strip()

            # Try to parse JSON response
            try:
                import json
                content_data = json.loads(result_text)

                # Add real images to the content
                if 'category' in content_data and isinstance(content_data['category'], dict):
                    category_name = content_data['category'].get('name', query)
                    content_data['category']['image'] = groq_service.search_for_reliable_image(category_name, "category")

                if 'author' in content_data and isinstance(content_data['author'], dict):
                    author_name = content_data['author'].get('name', 'professional author')
                    content_data['author']['image'] = groq_service.search_for_reliable_image(f"{author_name} portrait", "person")

                return content_data

            except json.JSONDecodeError:
                # Fallback: create structured content from text response
                return self._create_fallback_content(article_id, query, language, result_text)

        except Exception as e:
            print(f"Error generating article content: {str(e)}")
            return self._create_fallback_content(article_id, query, language)

    def _create_fallback_content(self, article_id, query, language, content_text=None):
        """Create fallback content when LLM generation fails"""
        # Initialize Groq service for image search
        groq_service = GroqLLMService()

        if language == 'ar':
            return {
                "id": article_id,
                "full_text": content_text or f"محتوى مفصل حول {query}. هذا المقال يقدم تحليلاً شاملاً للموضوع مع استعراض الجوانب المختلفة والتطورات الحديثة. يهدف هذا المحتوى إلى تقديم فهم شامل للقارئ حول {query} وتأثيراته على المجتمع والاقتصاد. كما يستكشف المقال التحديات والفرص المرتبطة بهذا الموضوع، ويقدم رؤى من خبراء مختصين في المجال. المقال مدعوم بأمثلة عملية ودراسات حالة توضح التطبيقات الواقعية للموضوع. يتناول المقال أيضاً التطورات التاريخية والاتجاهات المستقبلية المتعلقة بـ {query}، مما يوفر للقارئ نظرة شاملة ومتوازنة حول الموضوع.",
                "category": {
                    "name": "معلومات عامة",
                    "description": "فئة شاملة تغطي مواضيع متنوعة ومعلومات عامة مفيدة للقراء. تشمل هذه الفئة مجالات واسعة من المعرفة والعلوم والتكنولوجيا والثقافة. تهدف إلى تقديم محتوى عالي الجودة يساعد القراء على فهم العالم من حولهم بشكل أفضل. تتميز هذه الفئة بالتنوع والشمولية، حيث تغطي موضوعات تتراوح من العلوم الطبيعية إلى العلوم الإنسانية، ومن التكنولوجيا الحديثة إلى التاريخ والثقافة. كما تركز على تقديم المعلومات بطريقة مبسطة ومفهومة للجمهور العام، مع الحفاظ على الدقة العلمية والموضوعية في العرض.",
                    "wikipedia_link": "https://ar.wikipedia.org/wiki/معلومات_عامة",
                    "image": groq_service.search_for_reliable_image("معلومات عامة", "category")
                },
                "author": {
                    "name": "د. محمد الكاتب",
                    "profession": "كاتب وباحث",
                    "description": "خبير متخصص في الكتابة والبحث العلمي مع خبرة تزيد عن 20 عاماً في مجال التأليف والنشر. حاصل على درجة الدكتوراه في الأدب العربي ومؤلف لأكثر من 15 كتاباً في مجالات متنوعة. يعمل كأستاذ جامعي ومستشار تحريري لعدة مجلات علمية محكمة. له مساهمات بارزة في تطوير المحتوى العربي الرقمي وتبسيط المعلومات العلمية للجمهور العام. يتميز بأسلوبه الواضح والمباشر في الكتابة، ويحرص على تقديم المعلومات بطريقة شيقة ومفيدة.",
                    "wikipedia_link": "https://ar.wikipedia.org/wiki/محمد_الكاتب",
                    "image": groq_service.search_for_reliable_image("د. محمد الكاتب", "person")
                },
                "keywords": [f"{query}", "معلومات", "تحليل", "دراسة", "بحث", "علوم", "تكنولوجيا", "ثقافة", "تعليم", "معرفة"],
                "summary": f"ملخص شامل للمقال حول {query} يغطي النقاط الرئيسية والاستنتاجات المهمة. يقدم هذا الملخص نظرة عامة على الموضوع مع التركيز على الجوانب الأكثر أهمية وتأثيراً. يتناول التطورات الحديثة والاتجاهات المستقبلية، ويقدم تحليلاً متوازناً للتحديات والفرص المرتبطة بالموضوع.",
                "publish_date": "2024-01-15"
            }
        else:
            return {
                "id": article_id,
                "full_text": content_text or f"Detailed content about {query}. This article provides comprehensive analysis of the topic with various aspects and recent developments. The content aims to give readers a thorough understanding of {query} and its implications for society and economy. The article examines challenges and opportunities related to this topic, offering insights from field experts. It is supported by practical examples and case studies that illustrate real-world applications of the subject matter. The piece also explores historical developments and future trends related to {query}, providing readers with a comprehensive and balanced view of the topic. The article is designed to be both informative and accessible to readers with varying levels of expertise, ensuring that complex concepts are explained clearly while maintaining academic rigor.",
                "category": {
                    "name": "General Information",
                    "description": "A comprehensive category covering diverse topics and general information useful for readers. This category encompasses wide-ranging fields of knowledge including science, technology, culture, and education. It aims to provide high-quality content that helps readers better understand the world around them. The category is characterized by diversity and comprehensiveness, covering topics ranging from natural sciences to humanities, from modern technology to history and culture. It focuses on presenting information in a simplified and understandable way for the general public, while maintaining scientific accuracy and objectivity in presentation. The content is carefully curated to ensure relevance and educational value for a broad audience.",
                    "wikipedia_link": "https://en.wikipedia.org/wiki/General_knowledge",
                    "image": groq_service.search_for_reliable_image("General Information", "category")
                },
                "author": {
                    "name": "Dr. John Writer",
                    "profession": "writer and researcher",
                    "description": "Specialized expert in writing and research with over 20 years of experience in authoring and publishing. Holds a Ph.D. in Literature and is the author of more than 15 books across various fields. Works as a university professor and editorial consultant for several peer-reviewed scientific journals. Has made significant contributions to digital content development and simplifying scientific information for general audiences. Known for clear and direct writing style, and committed to presenting information in an engaging and useful manner. Regularly contributes to academic conferences and maintains active research in contemporary writing methodologies.",
                    "wikipedia_link": "https://en.wikipedia.org/wiki/John_Writer",
                    "image": groq_service.search_for_reliable_image("Dr. John Writer", "person")
                },
                "keywords": [f"{query}", "information", "analysis", "study", "research", "science", "technology", "culture", "education", "knowledge"],
                "summary": f"Comprehensive summary of the article about {query} covering key points and important conclusions. This summary provides an overview of the topic with focus on the most important and impactful aspects. It addresses recent developments and future trends, offering a balanced analysis of challenges and opportunities related to the subject matter.",
                "publish_date": "2024-01-15"
            }

class DepartmentInfoView(APIView):
    """
    API endpoint for retrieving department information

    POST /api/department/
    {
        "department": "IT",
        "language": "en"
    }
    """

    def post(self, request):
        """Generate department information using LLM"""

        # Validate request data
        try:
            department = request.data.get('department', '').strip()
            language = request.data.get('language', 'en')

            if not department:
                return Response({
                    'success': False,
                    'message': 'Department name or code is required',
                    'department': None
                }, status=status.HTTP_400_BAD_REQUEST)

            if language not in ['en', 'ar']:
                language = 'en'  # Default to English

        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid request data',
                'department': None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Initialize Groq LLM service
            groq_service = GroqLLMService()

            # Generate department information using LLM
            department_info = groq_service.generate_department_info(
                department_input=department,
                language=language
            )

            if department_info:
                return Response({
                    'success': True,
                    'message': 'Department information generated successfully',
                    'department': department_info
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to generate department information',
                    'department': None
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Department information generation failed: {str(e)}',
                'department': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealthCheckView(APIView):
    """Health check endpoint"""

    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Article Search API is running',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)

