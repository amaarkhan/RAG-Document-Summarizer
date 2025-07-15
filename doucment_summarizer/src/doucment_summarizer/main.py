#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from doucment_summarizer.crew import DocumentSummarizer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# --------------------------
# 🟢 MAIN RUN
# --------------------------
def run():
    """
    Main run function with continuous interactive query support.
    Users can ask multiple questions about documents.
    """
    import os
    
    # Look for a sample document in common locations
    sample_files = [
        'documents/sample.pdf',
        'documents/Agentic.pdf'
    ]
    
    filename = None
    for sample in sample_files:
        if os.path.exists(sample):
            filename = sample
            break
    
    if filename is None:
        print("No sample document found. Please place a document in the 'documents' folder.")
        print("Supported formats: PDF, TXT, DOCX, DOC, MD")
        return
    
    print(f"📄 Document loaded: {filename}")
    print("\n" + "="*60)
    print("🤖 Interactive Document Q&A System")
    print("="*60)
    print("\nYou can ask multiple questions about this document.")
    print("Examples:")
    print("- Summarize this document")
    print("- What are the key concepts discussed?")
    print("- What is ReWOO architecture?")
    print("- Extract main points from this document")
    print("\nType 'quit', 'exit', or 'bye' to stop.")
    print("-" * 60)
    
    crew_instance = DocumentSummarizer().crew()
    
    while True:
        try:
            user_query = input("\n🔍 Enter your question: ").strip()
            
            if not user_query:
                print("❌ Please enter a question.")
                continue
                
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Thank you for using the Document Q&A System!")
                break
            
            inputs = {
                'filename': filename,
                'query': user_query,
                'current_year': str(datetime.now().year)
            }

            print(f"\n🔄 Processing: '{user_query}'")
            print("-" * 40)
            
            result = crew_instance.kickoff(inputs=inputs)
            
            print("\n" + "✅ " + "="*48)
            print("RESPONSE COMPLETED")
            print("="*50)
            print(result)
            print("\n" + "="*50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Thank you for using the Document Q&A System!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again with a different question.")
    
    return None


# --------------------------
# 🔁 TRAINING FUNCTION
# --------------------------
def train():
    inputs = {
        'filename': 'your_file_path_here.pdf',
        'query': 'Summarize this document.',
        'current_year': str(datetime.now().year)
    }

    try:
        DocumentSummarizer().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while training the crew: {e}")
        return None


# --------------------------
# 🧪 TESTING FUNCTION
# --------------------------
def test():
    inputs = {
        'filename': 'your_file_path_here.pdf',
        'query': 'Summarize this document.',
        'current_year': str(datetime.now().year)
    }

    try:
        DocumentSummarizer().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],  # e.g., "gpt-4" or "claude"
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while testing the crew: {e}")
        return None


# --------------------------
# 🔁 REPLAY FUNCTION
# --------------------------
def replay():
    try:
        DocumentSummarizer().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        print(f"An error occurred while replaying the crew: {e}")
        return None


# 🛠️ Optionally use this if you're running as a script
if __name__ == "__main__":
    run()  # or call train(), test(), replay() depending on args
