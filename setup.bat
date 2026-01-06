 @echo off
echo ========================================
echo AI Resume Analyzer Setup
echo ========================================

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm

echo.
echo Initializing database...
python database/init_db.py

echo.
echo Creating uploads directory...
mkdir uploads 2>nul

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo python app.py
echo.
echo Then open your browser and go to:
echo http://localhost:5000
echo.
pause