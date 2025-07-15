#!/usr/bin/env python
"""
Flask Web Application for RAG Document Summarizer
"""
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from doucment_summarizer.crew import DocumentSummarizer
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = Flask(__name__)

# Global variables to store document and crew instance
current_document = None
crew_instance = None

def initialize_app():
    """Initialize the application with a document"""
    global current_document, crew_instance
    
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
    return render_template('index.html', document=current_document)

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