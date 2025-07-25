# Department Information API

## Overview

The Department API endpoint provides comprehensive information about organizational departments using **Large Language Models (LLM)** via Groq. This endpoint generates detailed department information **without any database operations**, including department names, codes, descriptions, responsibilities, objectives, and real logos.

## 🎯 **Key Features**

### ✅ No Database Operations
- Pure LLM-based department information generation
- No data persistence or retrieval from databases
- Real-time content generation for each request

### ✅ Flexible Input Support
- **Department Codes**: IT, HR, FIN, MKT, etc.
- **Full Names**: Information Technology, Human Resources, Finance, Marketing
- **Mixed Languages**: English and Arabic department names

### ✅ Comprehensive Information
- **Full Department Name**: Complete official name
- **Department Code**: Standard abbreviation (IT, HR, etc.)
- **Detailed Description**: 200+ word comprehensive description
- **Responsibilities**: List of key department responsibilities
- **Objectives**: Department goals and objectives
- **Real Logos**: Intelligent logo search with fallbacks

### ✅ Multi-language Support
- English (`en`)
- Arabic (`ar`)
- Language-specific content generation

## 📋 **API Endpoint**

### Department Information
**POST** `/api/department/`

Generate comprehensive department information based on department name or code.

**Request:**
```json
{
    "department": "IT",
    "language": "en"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Department information generated successfully",
    "department": {
        "name": "Information Technology",
        "code": "IT",
        "description": "The Information Technology department is a vital component of the organization, responsible for managing and maintaining all technological infrastructure and digital systems. This department oversees the implementation, operation, and security of computer systems, networks, software applications, and digital communication tools that enable the organization to function efficiently in today's digital landscape. The IT department plays a crucial role in digital transformation initiatives, ensuring that technology solutions align with business objectives and support organizational growth. They are responsible for maintaining cybersecurity protocols, managing data integrity, and providing technical support to all departments within the organization.",
        "responsibilities": [
            "Managing and coordinating Information Technology activities",
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
        "logo": "https://example.com/real-it-logo.png",
        "language": "en"
    }
}
```

## 🔧 **Supported Department Inputs**

### Common Department Codes
- **IT** → Information Technology
- **HR** → Human Resources  
- **FIN** → Finance
- **MKT** → Marketing
- **SAL** → Sales
- **OPS** → Operations
- **LEG** → Legal Affairs
- **ADM** → Administration
- **R&D** → Research and Development
- **SUP** → Support
- **SEC** → Security

### Full Department Names
- Information Technology
- Human Resources
- Finance Department
- Marketing Division
- Sales Team
- Operations Management
- Legal Affairs
- Administration
- Research and Development
- Customer Support
- Security Department

### Arabic Department Names
- تكنولوجيا المعلومات
- الموارد البشرية
- المالية
- التسويق
- المبيعات
- العمليات
- الشؤون القانونية
- الإدارة

## 🖼️ **Logo Search Strategy**

The API implements intelligent logo search with multiple fallback levels:

### 1. **Department-Specific Search**
- Searches for actual department logos
- Uses department name + "logo" keywords
- Filters for high-quality images

### 2. **Icon-Based Fallback**
- Maps departments to relevant icon categories
- IT → technology, computer, server
- HR → people, team, human resources
- Finance → money, calculator, accounting

### 3. **Generic Placeholder**
- Clean, professional placeholder with department code
- Consistent branding colors
- Readable department abbreviation

## 🧪 **Testing**

### Run Department API Tests
```bash
python test_department_api.py
```

### Run Complete API Tests
```bash
python test_api_endpoints.py
```

### Manual Testing with curl
```bash
# English IT Department
curl -X POST "http://127.0.0.1:8000/api/department/" \
  -H "Content-Type: application/json" \
  -d '{"department": "IT", "language": "en"}'

# Arabic HR Department  
curl -X POST "http://127.0.0.1:8000/api/department/" \
  -H "Content-Type: application/json" \
  -d '{"department": "الموارد البشرية", "language": "ar"}'

# Full Department Name
curl -X POST "http://127.0.0.1:8000/api/department/" \
  -H "Content-Type: application/json" \
  -d '{"department": "Information Technology", "language": "en"}'
```

## 📊 **Response Structure**

### Success Response
```json
{
    "success": true,
    "message": "Department information generated successfully",
    "department": {
        "name": "Full Department Name",
        "code": "DEPT_CODE", 
        "description": "200+ word detailed description...",
        "responsibilities": ["responsibility1", "responsibility2", ...],
        "objectives": ["objective1", "objective2", ...],
        "logo": "https://real-logo-url.com/logo.png",
        "language": "en"
    }
}
```

### Error Response
```json
{
    "success": false,
    "message": "Department name or code is required",
    "department": null
}
```

## 🚀 **Usage Examples**

### JavaScript/Frontend
```javascript
const response = await fetch('http://127.0.0.1:8000/api/department/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        department: 'HR',
        language: 'en'
    })
});

const data = await response.json();
if (data.success) {
    console.log('Department:', data.department.name);
    console.log('Code:', data.department.code);
    console.log('Logo:', data.department.logo);
}
```

### Python
```python
import requests

response = requests.post('http://127.0.0.1:8000/api/department/', json={
    'department': 'Finance',
    'language': 'en'
})

if response.status_code == 200:
    data = response.json()
    if data['success']:
        dept = data['department']
        print(f"Department: {dept['name']}")
        print(f"Code: {dept['code']}")
        print(f"Description: {dept['description'][:100]}...")
```

## 🔍 **Quality Guarantees**

### Content Requirements
- ✅ **Descriptions**: Minimum 200 words per department
- ✅ **Responsibilities**: 5+ key responsibilities listed
- ✅ **Objectives**: 5+ department objectives
- ✅ **Accuracy**: LLM-generated, contextually relevant content

### Logo Quality
- ✅ **Real Images**: Intelligent search for actual department logos
- ✅ **Fallback System**: Professional placeholders when needed
- ✅ **Consistency**: Uniform branding and quality standards

### Multi-language Support
- ✅ **Arabic**: Native Arabic content generation
- ✅ **English**: Professional English content
- ✅ **Cultural Adaptation**: Language-appropriate content style

## 🛠️ **Error Handling**

### Common Error Cases
1. **Missing Department**: Returns 400 with error message
2. **Invalid Language**: Defaults to English ('en')
3. **LLM Generation Failure**: Uses structured fallback content
4. **Network Issues**: Graceful degradation with placeholders

### Troubleshooting
- Ensure Django server is running: `python manage.py runserver 8000`
- Check GROQ_API_KEY environment variable
- Verify request format and required fields
- Use trailing slash in URL: `/api/department/`

## 🔗 **Integration with Other Endpoints**

The Department API complements the existing article search system:
- **Article Search**: `/api/search/` - Generate articles
- **Article Content**: `/api/content/` - Get detailed content  
- **Department Info**: `/api/department/` - Get department information
- **Health Check**: `/api/health/` - System status

All endpoints follow the same principles:
- No database operations
- LLM-based generation
- Real image integration
- Multi-language support
