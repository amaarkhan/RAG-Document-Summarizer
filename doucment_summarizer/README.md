# Document Summarizer Crew

Welcome to the Document Summarizer Crew project, powered by [crewAI](https://crewai.com). This intelligent document analysis system allows users to ask any question about their documents and get comprehensive answers using RAG (Retrieval Augmented Generation) technology.

## Features

- **Ask Multiple Questions**: Users can ask unlimited questions about their documents in an interactive session
- **Any Question Supported**: Ask for summaries, specific details, analysis, explanations, or any other document-related queries
- **Multiple File Formats**: Supports PDF, TXT, DOCX, DOC, and MD files
- **Intelligent Retrieval**: Uses semantic search to find relevant document sections
- **Comprehensive Answers**: Provides detailed responses based on document content
- **Interactive Interface**: Continuous Q&A session until you choose to exit

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

First, install uv if you haven't already:

```bash
pip install uv
```

Navigate to your project directory and install dependencies:

```bash
crewai install
```

### Configuration

**Add your Gemini API key to the `.env` file:**

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Place your documents in the `documents/` folder. Supported formats:
- PDF files
- Text files (.txt)
- Word documents (.docx, .doc)
- Markdown files (.md)

## Running the Project

### Option 1: Command Line Interface (CLI)
To start the interactive document Q&A system in the terminal:

```bash
crewai run
```

### Option 2: Web Interface
To start the web application:

```bash
uv run web_app
```

Or using the script:

```bash
python -m doucment_summarizer.app
```

The web interface will be available at: http://localhost:5000

## Features of the Web Interface

- **📁 File Upload**: Drag and drop or browse to upload documents
- **📚 Document Management**: View, select, and delete uploaded documents  
- **❓ Interactive Q&A**: Ask questions through a clean web interface
- **🤖 Real-time Processing**: Get AI-powered answers instantly
- **📱 Responsive Design**: Works on desktop and mobile devices
- **💡 Question Examples**: Built-in suggestions for better queries

The system will:
1. Find documents in the `documents/` folder
2. Start an interactive session where you can ask unlimited questions
3. Process each question using AI agents
4. Return comprehensive answers for each query
5. Continue until you type 'quit', 'exit', or 'bye'

## Example Questions You Can Ask

You can ask multiple questions in a single session:

- "Summarize this document"
- "What are the key concepts discussed?"
- "What is the main argument in this paper?"
- "Extract all the important statistics"
- "What are the conclusions and recommendations?"
- "Explain the methodology used"
- "What are the limitations mentioned?"
- "Who are the main authors or researchers cited?"
- Any specific question about the document content

**Interactive Session**: After each answer, you can immediately ask follow-up questions or explore different aspects of the document.

## How It Works

The system uses two AI agents:

1. **Document Chunking & Retrieval Expert**: Processes documents, creates embeddings, and retrieves relevant sections
2. **Document Analysis Expert**: Analyzes retrieved content and provides comprehensive answers

## Support

For support, questions, or feedback:
- Visit [crewAI documentation](https://docs.crewai.com)
- Check the [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join the Discord community](https://discord.com/invite/X4JWnZnxPb)
