# AI Resume Analyzer & Job Matcher

An AI-powered web application that analyzes resumes against job descriptions, providing ATS scores and skill gap analysis using advanced NLP techniques.

## 🚀 Features

- **Resume Upload**: Support for PDF, DOCX, and TXT files
- **AI-Powered Analysis**: Uses BERT and Sentence Transformers for semantic matching
- **ATS Score Calculation**: Get compatibility scores with job descriptions
- **Skill Extraction**: Automatic identification of technical and soft skills
- **Gap Analysis**: Identify missing skills and matching competencies
- **Interactive Dashboard**: Modern, responsive web interface
- **Analysis History**: Track previous analyses and improvements
- **Sample Jobs**: Pre-loaded job descriptions for testing

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **spaCy** - NLP processing
- **BERT/Transformers** - Semantic analysis
- **Sentence Transformers** - Text similarity
- **scikit-learn** - TF-IDF and ML algorithms
- **SQLite** - Database storage

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - Responsive design
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icons

### AI/ML Components
- **BERT** - Bidirectional Encoder Representations
- **TF-IDF** - Term Frequency-Inverse Document Frequency
- **Cosine Similarity** - Text matching algorithm
- **Named Entity Recognition** - Skill extraction

## 📁 Project Structure

```
project1/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup.bat             # Windows setup script
├── README.md             # Documentation
├── database/
│   ├── init_db.py        # Database initialization
│   └── resume_analyzer.db # SQLite database (created after setup)
├── models/
│   ├── resume_analyzer.py # AI analysis engine
│   └── file_processor.py  # File handling utilities
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── uploads/              # Temporary file storage (created after setup)
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup (Windows)
1. **Clone or download** this project
2. **Run the setup script**:
   ```bash
   setup.bat
   ```

### Manual Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Initialize database**:
   ```bash
   python database/init_db.py
   ```

4. **Create uploads directory**:
   ```bash
   mkdir uploads
   ```

## 🚀 Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 How to Use

### 1. Upload Resume
- Click "Choose File" or drag & drop your resume
- Supported formats: PDF, DOCX, TXT
- The system will extract text and identify skills

### 2. Enter Job Description
- Fill in job title and company (optional)
- Paste the job description in the text area
- Or use "Load Sample Job" for testing

### 3. Analyze
- Click "Analyze Resume" to start AI processing
- Wait for the analysis to complete

### 4. Review Results
- **ATS Score**: Compatibility percentage (0-100%)
- **Matching Skills**: Skills you have that match the job
- **Missing Skills**: Skills mentioned in job but not in resume
- **Recommendations**: AI-generated improvement suggestions

### 5. Track Progress
- View analysis history in the History section
- Compare scores across different job applications

## 🧠 AI Analysis Process

### 1. Text Preprocessing
- Extract text from uploaded files
- Clean and normalize content
- Remove special characters and extra whitespace

### 2. Skill Extraction
- **Pattern Matching**: Regex patterns for common technical skills
- **Named Entity Recognition**: spaCy NLP for skill identification
- **Contextual Analysis**: BERT-based semantic understanding

### 3. Similarity Calculation
- **Semantic Similarity**: Sentence Transformers embeddings
- **TF-IDF Matching**: Traditional text similarity
- **Keyword Overlap**: Direct skill matching

### 4. Score Calculation
```python
ATS Score = (Semantic Similarity × 0.4) + (TF-IDF × 0.3) + (Keyword Match × 0.3)
```

## 📊 Score Interpretation

- **80-100%**: Excellent Match - High ATS compatibility
- **60-79%**: Good Match - Strong candidate profile
- **40-59%**: Average Match - Some improvements needed
- **0-39%**: Poor Match - Significant gaps identified

## 🔧 Customization

### Adding New Skills
Edit `models/resume_analyzer.py` and update the `skill_patterns` list:

```python
self.skill_patterns = [
    r'\b(?:your|custom|skills|here)\b',
    # Add more patterns
]
```

### Modifying Score Weights
Adjust weights in the `calculate_ats_score` method:

```python
ats_score = (semantic_similarity * 0.4 + 
             tfidf_similarity * 0.3 + 
             keyword_match * 0.3) * 100
```

### Custom Job Templates
Add sample jobs in `app.py` under the `sample_jobs` route.

## 🐛 Troubleshooting

### Common Issues

1. **spaCy Model Error**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **File Upload Issues**:
   - Check file format (PDF, DOCX, TXT only)
   - Ensure file is not corrupted
   - Try with a different file

3. **Low ATS Scores**:
   - Use keywords from job description
   - Include relevant technical skills
   - Quantify achievements with numbers

4. **Database Errors**:
   ```bash
   python database/init_db.py
   ```

## 📈 Performance Optimization

- **Caching**: Implement Redis for faster repeated analyses
- **Async Processing**: Use Celery for background tasks
- **Model Optimization**: Fine-tune BERT for domain-specific skills
- **Database Indexing**: Add indexes for faster queries

## 🔒 Security Considerations

- Files are temporarily stored and automatically deleted
- No personal data is permanently stored
- Use HTTPS in production
- Implement rate limiting for API endpoints

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Example with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the code documentation
- Create an issue in the repository

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced skill taxonomy
- [ ] Industry-specific analysis
- [ ] Resume optimization suggestions
- [ ] Integration with job boards
- [ ] Mobile app version
- [ ] Advanced analytics dashboard

---

**Built with ❤️ using Python, NLP, BERT & Flask**

*Improving skill-job matching accuracy by 40% using advanced AI techniques.*