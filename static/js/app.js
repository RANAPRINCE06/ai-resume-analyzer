// AI Resume Analyzer Frontend JavaScript

class ResumeAnalyzer {
    constructor() {
        this.resumeUploaded = false;
        this.sampleJobs = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSampleJobs();
        this.loadHistory();
    }

    setupEventListeners() {
        // File upload
        const fileInput = document.getElementById('resumeFile');
        const uploadArea = document.getElementById('uploadArea');

        fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.uploadFile(files[0]);
            }
        });

        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            await this.uploadFile(file);
        }
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('resume', file);

        try {
            this.showLoading('Uploading and processing resume...');
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                this.displayUploadSuccess(result);
                this.resumeUploaded = true;
                document.getElementById('analyze').style.display = 'block';
                this.scrollToSection('analyze');
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Error uploading file: ' + error.message);
        }
    }

    displayUploadSuccess(result) {
        const uploadResult = document.getElementById('uploadResult');
        uploadResult.innerHTML = `
            <div class="alert alert-success fade-in-up">
                <h5><i class="fas fa-check-circle me-2"></i>Resume Uploaded Successfully!</h5>
                <p><strong>File:</strong> ${result.filename}</p>
                <p><strong>Extracted Skills:</strong></p>
                <div class="skills-container">
                    ${result.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                </div>
                <div class="mt-3">
                    <small class="text-muted">Preview: ${result.text_preview}</small>
                </div>
            </div>
        `;
        uploadResult.style.display = 'block';
    }

    async loadSampleJobs() {
        try {
            const response = await fetch('/sample-jobs');
            const result = await response.json();
            this.sampleJobs = result.jobs;
        } catch (error) {
            console.error('Error loading sample jobs:', error);
        }
    }

    async analyzeResume() {
        if (!this.resumeUploaded) {
            this.showError('Please upload a resume first');
            return;
        }

        const jobTitle = document.getElementById('jobTitle').value;
        const company = document.getElementById('company').value;
        const jobDescription = document.getElementById('jobDescription').value;

        if (!jobDescription.trim()) {
            this.showError('Please enter a job description');
            return;
        }

        try {
            this.showLoading('Analyzing resume with AI...');

            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    job_title: jobTitle,
                    company: company,
                    job_description: jobDescription
                })
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                this.displayAnalysisResults(result);
                this.loadHistory(); // Refresh history
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Error analyzing resume: ' + error.message);
        }
    }

    displayAnalysisResults(result) {
        const analysis = result.analysis;
        const resultsDiv = document.getElementById('analysisResults');
        
        // Determine score category
        let scoreClass = 'poor';
        let scoreText = 'Needs Improvement';
        
        if (analysis.ats_score >= 80) {
            scoreClass = 'excellent';
            scoreText = 'Excellent Match';
        } else if (analysis.ats_score >= 60) {
            scoreClass = 'good';
            scoreText = 'Good Match';
        } else if (analysis.ats_score >= 40) {
            scoreClass = 'average';
            scoreText = 'Average Match';
        }

        resultsDiv.innerHTML = `
            <div class="fade-in-up">
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="ats-score ${scoreClass}">
                            <div>${analysis.ats_score}%</div>
                            <small>${scoreText}</small>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <h5>Job Match Analysis</h5>
                        <p><strong>Position:</strong> ${result.job_title} at ${result.company}</p>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-${scoreClass === 'excellent' ? 'success' : scoreClass === 'good' ? 'info' : scoreClass === 'average' ? 'warning' : 'danger'}" 
                                 style="width: ${analysis.ats_score}%"></div>
                        </div>
                        <small class="text-muted">ATS Compatibility Score</small>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header bg-success text-white">
                                <h6 class="mb-0"><i class="fas fa-check me-2"></i>Matching Skills (${analysis.matching_skills.length})</h6>
                            </div>
                            <div class="card-body">
                                ${analysis.matching_skills.length > 0 ? 
                                    analysis.matching_skills.map(skill => `<span class="skill-tag matching">${skill}</span>`).join('') :
                                    '<p class="text-muted">No matching skills found</p>'
                                }
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6 mb-4">
                        <div class="card">
                            <div class="card-header bg-danger text-white">
                                <h6 class="mb-0"><i class="fas fa-times me-2"></i>Missing Skills (${analysis.missing_skills.length})</h6>
                            </div>
                            <div class="card-body">
                                ${analysis.missing_skills.length > 0 ? 
                                    analysis.missing_skills.map(skill => `<span class="skill-tag missing">${skill}</span>`).join('') :
                                    '<p class="text-success">Great! No missing skills detected</p>'
                                }
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-12 mb-4">
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h6 class="mb-0"><i class="fas fa-user-tie me-2"></i>Your Resume Skills (${analysis.resume_skills.length})</h6>
                            </div>
                            <div class="card-body">
                                ${analysis.resume_skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>

                ${analysis.recommendations.length > 0 ? `
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-header bg-warning text-dark">
                                <h6 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Recommendations</h6>
                            </div>
                            <div class="card-body">
                                ${analysis.recommendations.map(rec => `
                                    <div class="recommendation-item">
                                        <i class="fas fa-arrow-right me-2"></i>${rec}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
                ` : ''}
            </div>
        `;

        document.getElementById('results').style.display = 'block';
        this.scrollToSection('results');
    }

    async loadHistory() {
        try {
            const response = await fetch('/history');
            const result = await response.json();
            
            if (result.history && result.history.length > 0) {
                this.displayHistory(result.history);
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    displayHistory(history) {
        const historyDiv = document.getElementById('historyResults');
        
        historyDiv.innerHTML = `
            <div class="table-responsive">
                <table class="table table-hover history-table">
                    <thead>
                        <tr>
                            <th>Resume</th>
                            <th>Job Title</th>
                            <th>Company</th>
                            <th>ATS Score</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${history.map(item => `
                            <tr>
                                <td><i class="fas fa-file-alt me-2"></i>${item.filename}</td>
                                <td>${item.job_title}</td>
                                <td>${item.company}</td>
                                <td>
                                    <span class="badge bg-${item.ats_score >= 70 ? 'success' : item.ats_score >= 50 ? 'warning' : 'danger'}">
                                        ${item.ats_score}%
                                    </span>
                                </td>
                                <td>${new Date(item.analyzed_at).toLocaleDateString()}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    showLoading(message = 'Processing...') {
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        document.querySelector('#loadingModal .modal-body h5').textContent = message;
        modal.show();
    }

    hideLoading() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }

    showError(message) {
        alert('Error: ' + message);
    }

    scrollToSection(sectionId) {
        document.getElementById(sectionId).scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Global functions
function loadSampleJob() {
    const analyzer = window.resumeAnalyzer;
    if (analyzer.sampleJobs.length > 0) {
        const randomJob = analyzer.sampleJobs[Math.floor(Math.random() * analyzer.sampleJobs.length)];
        document.getElementById('jobTitle').value = randomJob.title;
        document.getElementById('company').value = randomJob.company;
        document.getElementById('jobDescription').value = randomJob.description;
    }
}

function analyzeResume() {
    window.resumeAnalyzer.analyzeResume();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.resumeAnalyzer = new ResumeAnalyzer();
});