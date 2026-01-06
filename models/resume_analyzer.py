import spacy
import re
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class ResumeAnalyzer:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Please install spacy model: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
        
        # Download NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        
        # Common skills patterns
        self.skill_patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|php|ruby|go|rust|swift)\b',
            r'\b(?:react|angular|vue|node\.js|express|django|flask|spring)\b',
            r'\b(?:sql|mysql|postgresql|mongodb|redis|elasticsearch)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|jenkins|git)\b',
            r'\b(?:machine learning|deep learning|nlp|computer vision|data science)\b',
            r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy)\b'
        ]
    
    def extract_text_from_resume(self, text):
        """Clean and preprocess resume text"""
        # Remove extra whitespace and special characters
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\-\+#]', ' ', text)
        return text.strip()
    
    def extract_skills(self, text):
        """Extract skills from text using pattern matching and NLP"""
        skills = set()
        text_lower = text.lower()
        
        # Pattern-based extraction
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.update(matches)
        
        # NLP-based extraction
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                    skills.add(ent.text.lower())
        
        # Common technical skills
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'node.js',
            'sql', 'mongodb', 'aws', 'docker', 'git', 'machine learning',
            'data analysis', 'project management', 'agile', 'scrum'
        ]
        
        for skill in tech_skills:
            if skill in text_lower:
                skills.add(skill)
        
        return list(skills)
    
    def calculate_ats_score(self, resume_text, job_description):
        """Calculate ATS compatibility score"""
        # Sentence transformer similarity
        resume_embedding = self.sentence_model.encode([resume_text])
        job_embedding = self.sentence_model.encode([job_description])
        semantic_similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        # TF-IDF similarity
        try:
            tfidf_matrix = self.tfidf.fit_transform([resume_text, job_description])
            tfidf_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            tfidf_similarity = 0
        
        # Keyword matching
        resume_skills = set(self.extract_skills(resume_text))
        job_skills = set(self.extract_skills(job_description))
        
        if job_skills:
            keyword_match = len(resume_skills.intersection(job_skills)) / len(job_skills)
        else:
            keyword_match = 0
        
        # Weighted score
        ats_score = (semantic_similarity * 0.4 + tfidf_similarity * 0.3 + keyword_match * 0.3) * 100
        
        return min(ats_score, 100)
    
    def find_missing_skills(self, resume_text, job_description):
        """Find skills mentioned in job description but missing from resume"""
        resume_skills = set(self.extract_skills(resume_text))
        job_skills = set(self.extract_skills(job_description))
        
        missing_skills = job_skills - resume_skills
        matching_skills = job_skills.intersection(resume_skills)
        
        return list(missing_skills), list(matching_skills)
    
    def analyze_resume(self, resume_text, job_description):
        """Complete resume analysis"""
        # Clean texts
        resume_text = self.extract_text_from_resume(resume_text)
        job_description = self.extract_text_from_resume(job_description)
        
        # Calculate ATS score
        ats_score = self.calculate_ats_score(resume_text, job_description)
        
        # Find missing and matching skills
        missing_skills, matching_skills = self.find_missing_skills(resume_text, job_description)
        
        # Extract all skills from resume
        all_resume_skills = self.extract_skills(resume_text)
        
        return {
            'ats_score': round(ats_score, 2),
            'missing_skills': missing_skills,
            'matching_skills': matching_skills,
            'resume_skills': all_resume_skills,
            'recommendations': self.generate_recommendations(ats_score, missing_skills)
        }
    
    def generate_recommendations(self, ats_score, missing_skills):
        """Generate improvement recommendations"""
        recommendations = []
        
        if ats_score < 60:
            recommendations.append("Consider restructuring your resume to better match job requirements")
        
        if missing_skills:
            recommendations.append(f"Consider adding these skills: {', '.join(missing_skills[:5])}")
        
        if ats_score < 40:
            recommendations.append("Use more keywords from the job description")
            recommendations.append("Quantify your achievements with numbers and metrics")
        
        return recommendations