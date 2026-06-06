from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__)

BOOKS = [
    {
        "id": "book1",
        "title": "Till Operating Programme",
        "subtitle": "2-Week Short Course",
        "description": "Cash Handling | EcoCash | Bank Transfers | Card Swipe. Zimbabwe's most practical till operating course. No O-Level required.",
        "programme": "2-Week Short Course",
        "badge": "SHORT COURSE",
        "badge_color": "green",
        "pdf": "Book1-Till-Operating-Programme.pdf",
        "docx": "Book1-Till-Operating-Programme.docx",
        "icon": "🏪",
        "topics": ["Cash Handling", "EcoCash Payments", "Bank Transfers", "Card Swipe", "Float Management", "Till Balancing"],
    },
    {
        "id": "book2",
        "title": "Computer Basics & Typing",
        "subtitle": "Month 1 — 6-Month Diploma",
        "description": "Learn the fundamentals of using a computer, keyboard skills, and touch-typing from scratch.",
        "programme": "6-Month Diploma",
        "badge": "MONTH 1",
        "badge_color": "blue",
        "pdf": "Book2-Month1-Computer-Basics-Typing.pdf",
        "docx": "Book2-Month1-Computer-Basics-Typing.docx",
        "icon": "💻",
        "topics": ["Computer Hardware", "Windows Basics", "Keyboard Skills", "Touch Typing", "File Management", "Basic Troubleshooting"],
    },
    {
        "id": "book3",
        "title": "Microsoft Word",
        "subtitle": "Month 2 — 6-Month Diploma",
        "description": "Master Microsoft Word for professional documents, CVs, letters, and reports.",
        "programme": "6-Month Diploma",
        "badge": "MONTH 2",
        "badge_color": "blue",
        "pdf": "Book3-Month2-Microsoft-Word.pdf",
        "docx": "Book3-Month2-Microsoft-Word.docx",
        "icon": "📝",
        "topics": ["Formatting Text", "Paragraphs & Styles", "Tables", "Mail Merge", "CVs & Letters", "Printing Documents"],
    },
    {
        "id": "book4",
        "title": "Microsoft Excel",
        "subtitle": "Month 3 — 6-Month Diploma",
        "description": "Spreadsheets, formulas, budgets, and data analysis for business and employment.",
        "programme": "6-Month Diploma",
        "badge": "MONTH 3",
        "badge_color": "blue",
        "pdf": "Book4-Month3-Microsoft-Excel.pdf",
        "docx": "Book4-Month3-Microsoft-Excel.docx",
        "icon": "📊",
        "topics": ["Spreadsheet Basics", "Formulas & Functions", "Charts & Graphs", "Budget Templates", "Data Sorting", "Business Reports"],
    },
    {
        "id": "book5",
        "title": "Microsoft PowerPoint",
        "subtitle": "Month 4 — 6-Month Diploma",
        "description": "Create professional presentations for business, school, and job applications.",
        "programme": "6-Month Diploma",
        "badge": "MONTH 4",
        "badge_color": "blue",
        "pdf": "Book5-Month4-Microsoft-PowerPoint.pdf",
        "docx": "Book5-Month4-Microsoft-PowerPoint.docx",
        "icon": "🎯",
        "topics": ["Slide Design", "Transitions & Animations", "Images & Charts", "Speaker Notes", "Business Presentations", "Printing Handouts"],
    },
    {
        "id": "book6",
        "title": "Email & Internet",
        "subtitle": "Month 5 — 6-Month Diploma",
        "description": "Professional email communication, internet research, online safety, and Gmail.",
        "programme": "6-Month Diploma",
        "badge": "MONTH 5",
        "badge_color": "blue",
        "pdf": "Book6-Month5-Email-Internet.pdf",
        "docx": "Book6-Month5-Email-Internet.docx",
        "icon": "🌐",
        "topics": ["Gmail Setup", "Professional Emails", "Internet Research", "Online Safety", "Google Drive", "Video Calls"],
    },
    {
        "id": "book7",
        "title": "Social Media & Business",
        "subtitle": "Month 6 — 6-Month Diploma",
        "description": "Use social media for business: Facebook, WhatsApp Business, TikTok, and digital marketing.",
        "programme": "6-Month Diploma",
        "badge": "MONTH 6",
        "badge_color": "blue",
        "pdf": "Book7-Month6-Social-Media-Business.pdf",
        "docx": "Book7-Month6-Social-Media-Business.docx",
        "icon": "📱",
        "topics": ["WhatsApp Business", "Facebook Pages", "TikTok for Business", "Digital Marketing", "Online Advertising", "Building Your Brand"],
    },
]

@app.route("/")
def index():
    return render_template("index.html", books=BOOKS)

@app.route("/download/pdf/<filename>")
def download_pdf(filename):
    safe_files = [b["pdf"] for b in BOOKS]
    if filename not in safe_files:
        abort(404)
    return send_from_directory(
        os.path.join(app.root_path, "static", "pdfs"),
        filename,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )

@app.route("/download/docx/<filename>")
def download_docx(filename):
    safe_files = [b["docx"] for b in BOOKS]
    if filename not in safe_files:
        abort(404)
    return send_from_directory(
        os.path.join(app.root_path, "static", "docx"),
        filename,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
