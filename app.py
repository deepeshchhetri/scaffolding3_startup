"""
app.py
Flask application template for the warm-up assignment

Students need to implement the API endpoints as specified in the assignment.
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor
import traceback

app = Flask(__name__)
preprocessor = TextPreprocessor()

@app.route('/')
def home():
    """Render a simple HTML form for URL input"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Text preprocessing service is running"
    })

@app.route('/api/clean', methods=['POST'])
def clean_text():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate that JSON was sent
        if not data or 'url' not in data:
            return jsonify({"success": False, "error": "No URL provided"}), 400

        # Extract URL from the JSON
        url = data['url'].strip()

        # Validate URL (should be .txt)
        if not url.endswith('.txt'):
            return jsonify({"success": False, "error": "URL must point to a .txt file"}), 400

        # Fetch raw text from URL
        raw_text = preprocessor.fetch_from_url(url)

        # Clean the text
        cleaned_text = preprocessor.clean_gutenberg_text(raw_text)

        # Normalize the text
        normalized_text = preprocessor.normalize_text(cleaned_text)

        # Get statistics
        statistics = preprocessor.get_text_statistics(normalized_text)

        # Create summary
        summary = preprocessor.create_summary(cleaned_text, num_sentences=3)

        # Return JSON response
        return jsonify({
            "success": True,
            "cleaned_text": cleaned_text,
            "statistics": statistics,
            "summary": summary
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate that JSON was sent
        if not data or 'text' not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        # Extract text from the JSON
        text = data['text']

        # Get statistics
        statistics = preprocessor.get_text_statistics(text)

        # Return JSON response
        return jsonify({
            "success": True,
            "statistics": statistics
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print("   GET  /           - Web interface")
    print("   GET  /health     - Health check")
    print("   POST /api/clean  - Clean text from URL")
    print("   POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")

    app.run(debug=True, port=5000, host='0.0.0.0')