from flask import Flask, request, render_template, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
import docx
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from nlp_utils import compute_keywords, compute_match, compute_similarity_bert, generate_suggestions

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path, ext):
    if ext == 'pdf':
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif ext == 'docx':
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        resume_file = request.files.get('resume')
        job_description = request.form.get('job_description')
        model = request.form.get('model', 'nltk').lower()

        if not resume_file or not job_description:
            return jsonify({'error': 'Resume and job description are required.'}), 400

        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(file_path)

            ext = filename.rsplit('.', 1)[1].lower()
            resume_text = extract_text(file_path, ext)

            resume_keywords = compute_keywords(resume_text, model)
            jd_keywords = compute_keywords(job_description, model)
            if not resume_keywords or not jd_keywords:
                return jsonify({'error': 'Unable to extract keywords. Try a different model.'}), 500

            matched_keywords, missing_keywords, match_score = compute_match(resume_keywords, jd_keywords)
            semantic_score = round(compute_similarity_bert(resume_text, job_description) * 100, 2)

            suggestions = generate_suggestions(missing_keywords, match_score)

            # Save to session for PDF report
            session['report_data'] = {
                'match_score': match_score,
                'semantic_score': semantic_score,
                'missing_keywords': list(missing_keywords),
                'suggestions': suggestions
            }

            return jsonify({
                'match_score': match_score,
                'semantic_score': semantic_score,
                'missing_keywords': list(missing_keywords),
                'suggestions': suggestions
            })

        return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_report')
def download_report():
    report = session.get('report_data')
    if not report:
        return "No report available. Please analyze a resume first.", 400

    match_score = report.get('match_score', 0)
    semantic_score = report.get('semantic_score', 0)
    missing_keywords = report.get('missing_keywords', [])
    suggestions = report.get('suggestions', [])

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 40
    line_height = 20

    def draw_line(text, font_size=12, bold=False, indent=0):
        nonlocal y
        if y < 50:  # Create new page if near bottom
            c.showPage()
            y = height - 40
        c.setFont("Helvetica-Bold" if bold else "Helvetica", font_size)
        c.drawString(40 + indent, y, text)
        y -= line_height

    # Header
    draw_line("AI Career Coach - Resume Analysis Report", 14, bold=True)
    draw_line("------------------------------------------------------")

    # Scores
    draw_line(f"Match Score: {match_score}%", bold=True)
    draw_line(f"Semantic Score (BERT): {semantic_score}%", bold=True)
    draw_line("")

    # Missing Keywords
    draw_line("Missing Keywords:", bold=True)
    if missing_keywords:
        for kw in missing_keywords:
            draw_line(f"• {kw}", indent=20)
    else:
        draw_line("None", indent=20)
    draw_line("")

    # Suggestions
    draw_line("Suggestions:", bold=True)
    if suggestions:
        for s in suggestions:
            draw_line(f"- {s}", indent=20)
    else:
        draw_line("None", indent=20)

    # Save PDF
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="career_analysis_report.pdf",
        mimetype="application/pdf"
    )

if __name__ == '__main__':
    app.run(debug=True)
