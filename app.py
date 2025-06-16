from flask import Flask, render_template, request, jsonify
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files or 'jd' not in request.form:
            return jsonify({"error": "Missing resume or job description"}), 400

        resume_file = request.files['resume']
        job_desc = request.form['jd']

        if resume_file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        resume_text = ""
        with fitz.open(stream=resume_file.read(), filetype="pdf") as doc:
            for page in doc:
                resume_text += page.get_text()

        if not resume_text.strip():
            return jsonify({"error": "Could not extract any text from PDF."}), 400

        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        score = round(similarity * 100, 2)

        resume_words = set(resume_text.lower().split())
        jd_words = set(job_desc.lower().split())
        missing = list(jd_words - resume_words)

        feedback = "Excellent match!" if score >= 80 else "Good match!" if score >= 60 else "Moderate match." if score >= 40 else "Needs improvement."

        return jsonify({
            "score": score,
            "feedback": feedback,
            "missing": missing[:20]
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
