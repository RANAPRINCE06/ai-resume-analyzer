import PyPDF2
import docx
import os
from werkzeug.utils import secure_filename

class FileProcessor:
    def __init__(self):
        self.allowed_extensions = {'pdf', 'docx', 'txt'}
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    
    def process_uploaded_file(self, file):
        """Process uploaded file and extract text"""
        if not file or not self.allowed_file(file.filename):
            return None, "Invalid file type. Please upload PDF, DOCX, or TXT files."
        
        filename = secure_filename(file.filename)
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Extract text based on file extension
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            text = self.extract_text_from_docx(file_path)
        elif file_extension == 'txt':
            text = self.extract_text_from_txt(file_path)
        else:
            return None, "Unsupported file format"
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        if not text.strip():
            return None, "Could not extract text from file"
        
        return text, None