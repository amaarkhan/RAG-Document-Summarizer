#!/usr/bin/env python
"""
Flask Web Application for RAG Document Summarizer
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime
from doucment_summarizer.crew import DocumentSummarizer
import warnings
from werkzeug.utils import secure_filename

# Suppress warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'documents'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx', 'doc', 'md'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Global variables to store document and crew instance
current_document = None
crew_instance = None

def initialize_app():
    """Initialize the application with a document"""
    global current_document, crew_instance
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Look for a sample document in common locations
    sample_files = [
        'documents/sample.pdf',
        'documents/Agentic.pdf'
    ]
    
    for sample in sample_files:
        if os.path.exists(sample):
            current_document = sample
            break
    
    if current_document:
        try:
            crew_instance = DocumentSummarizer().crew()
            print(f"📄 Document loaded: {current_document}")
            return True
        except Exception as e:
            print(f"Error initializing crew: {e}")
            return False
    return False

@app.route('/')
def index():
    """Main page"""
    # Get list of uploaded documents
    uploaded_docs = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            if allowed_file(file):
                uploaded_docs.append(file)
    
    return render_template('index.html', document=current_document, uploaded_docs=uploaded_docs)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'document' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['document']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Use secure_filename equivalent
            filename = file.filename
            # Basic security: remove dangerous characters
            filename = "".join(c for c in filename if c.isalnum() or c in '._-')
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update current document to the newly uploaded one
            global current_document, crew_instance
            current_document = filepath
            
            # Reinitialize crew with new document
            try:
                crew_instance = DocumentSummarizer().crew()
                print(f"📄 New document uploaded and loaded: {current_document}")
                
                return jsonify({
                    'success': True,
                    'message': f'Document "{filename}" uploaded successfully!',
                    'filename': filename
                })
            except Exception as e:
                print(f"Error initializing crew with new document: {e}")
                return jsonify({'error': f'Document uploaded but failed to initialize: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Invalid file type. Only PDF, TXT, DOCX, DOC, and MD files are allowed.'}), 400
            
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500

@app.route('/select_document', methods=['POST'])
def select_document():
    """Handle document selection"""
    try:
        data = request.get_json()
        filename = data.get('filename', '').strip()
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'Document not found'}), 404
        
        # Update current document
        global current_document, crew_instance
        current_document = filepath
        
        # Reinitialize crew with selected document
        try:
            crew_instance = DocumentSummarizer().crew()
            print(f"📄 Document selected: {current_document}")
            
            return jsonify({
                'success': True,
                'message': f'Document "{filename}" selected successfully!',
                'filename': filename
            })
        except Exception as e:
            print(f"Error initializing crew with selected document: {e}")
            return jsonify({'error': f'Failed to initialize with selected document: {str(e)}'}), 500
            
    except Exception as e:
        print(f"❌ Error selecting document: {e}")
        return jsonify({'error': f'Error selecting document: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question submission"""
    try:
        data = request.get_json()
        user_query = data.get('question', '').strip()
        
        print(f"🔍 Received question: {user_query}")
        
        if not user_query:
            return jsonify({'error': 'Please enter a question'}), 400
            
        if not current_document:
            return jsonify({'error': 'No document loaded'}), 400
            
        if not crew_instance:
            return jsonify({'error': 'Crew not initialized'}), 500
        
        inputs = {
            'filename': current_document,
            'query': user_query,
            'current_year': str(datetime.now().year)
        }
        
        print(f"🔄 Processing question: {user_query}")
        result = crew_instance.kickoff(inputs=inputs)
        
        print(f"✅ Response completed for: {user_query}")
        
        return jsonify({
            'answer': str(result),
            'document': current_document,
            'question': user_query
        })
        
    except Exception as e:
        print(f"❌ Error processing question: {e}")
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'document_loaded': current_document is not None,
        'crew_initialized': crew_instance is not None
    })

def main():
    """Main function to run the Flask app"""
    print("🚀 Starting RAG Document Summarizer Web App...")
    
    if not initialize_app():
        print("❌ Failed to initialize app. Please ensure a document is available in the 'documents' folder.")
        return
    
    print("✅ App initialized successfully!")
    print("🌐 Starting web server on http://127.0.0.1:5000")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()