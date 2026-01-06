from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
import json
from datetime import datetime
from models.resume_analyzer import ResumeAnalyzer
from models.file_processor import FileProcessor

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Initialize components
analyzer = ResumeAnalyzer()
file_processor = FileProcessor()

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join('database', 'resume_analyzer.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Process file
        text, error = file_processor.process_uploaded_file(file)
        if error:
            return jsonify({'error': error}), 400
        
        # Extract skills
        skills = analyzer.extract_skills(text)
        
        # Store in session for analysis
        session['resume_text'] = text
        session['resume_filename'] = file.filename
        session['resume_skills'] = skills
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'skills': skills,
            'text_preview': text[:500] + '...' if len(text) > 500 else text
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume against job description"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        job_title = data.get('job_title', 'Job Position')
        company = data.get('company', 'Company')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        if 'resume_text' not in session:
            return jsonify({'error': 'Please upload a resume first'}), 400
        
        resume_text = session['resume_text']
        
        # Perform analysis
        analysis_result = analyzer.analyze_resume(resume_text, job_description)
        
        # Save to database
        conn = get_db_connection()
        
        # Save job description
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO job_descriptions (title, company, description, required_skills)
            VALUES (?, ?, ?, ?)
        ''', (job_title, company, job_description, json.dumps(analyzer.extract_skills(job_description))))
        
        job_id = cursor.lastrowid
        
        # Save resume
        cursor.execute('''
            INSERT INTO resumes (filename, content, skills)
            VALUES (?, ?, ?)
        ''', (session.get('resume_filename', 'resume.txt'), resume_text, json.dumps(session.get('resume_skills', []))))
        
        resume_id = cursor.lastrowid
        
        # Save analysis result
        cursor.execute('''
            INSERT INTO analysis_results (resume_id, job_id, ats_score, missing_skills, matching_skills)
            VALUES (?, ?, ?, ?, ?)
        ''', (resume_id, job_id, analysis_result['ats_score'], 
              json.dumps(analysis_result['missing_skills']),
              json.dumps(analysis_result['matching_skills'])))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'job_title': job_title,
            'company': company
        })
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500

@app.route('/history')
def analysis_history():
    """Get analysis history"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ar.*, r.filename, jd.title, jd.company, ar.analyzed_at
            FROM analysis_results ar
            JOIN resumes r ON ar.resume_id = r.id
            JOIN job_descriptions jd ON ar.job_id = jd.id
            ORDER BY ar.analyzed_at DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            history.append({
                'id': row['id'],
                'filename': row['filename'],
                'job_title': row['title'],
                'company': row['company'],
                'ats_score': row['ats_score'],
                'analyzed_at': row['analyzed_at']
            })
        
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': f'Error fetching history: {str(e)}'}), 500

@app.route('/sample-jobs')
def sample_jobs():
    """Get sample job descriptions"""
    sample_jobs = [
        {
            'title': 'Senior Python Developer',
            'company': 'Tech Corp',
            'description': '''We are looking for a Senior Python Developer with 5+ years of experience. 
            Required skills: Python, Django, Flask, PostgreSQL, AWS, Docker, Git, REST APIs, 
            Machine Learning, Data Analysis, Agile methodology. Experience with React and 
            JavaScript is a plus. Strong problem-solving skills and team collaboration required.'''
        },
        {
            'title': 'Data Scientist',
            'company': 'AI Solutions Inc',
            'description': '''Seeking a Data Scientist to join our AI team. Must have experience with 
            Python, R, Machine Learning, Deep Learning, TensorFlow, PyTorch, Pandas, NumPy, 
            Scikit-learn, SQL, Statistics, Data Visualization, Jupyter Notebooks. 
            Experience with NLP and Computer Vision preferred.'''
        },
        {
            'title': 'Full Stack Developer',
            'company': 'StartupXYZ',
            'description': '''Full Stack Developer needed for fast-paced startup environment. 
            Required: JavaScript, React, Node.js, Express, MongoDB, HTML5, CSS3, Git, 
            RESTful APIs, Agile development. Nice to have: TypeScript, GraphQL, AWS, Docker.'''
        }
    ]
    
    return jsonify({'jobs': sample_jobs})

if __name__ == '__main__':
    # Initialize database
    from database.init_db import init_db
    init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)