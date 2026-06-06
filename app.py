from flask import (
    Flask, render_template, send_from_directory,
    abort, request, redirect, url_for, session
)
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ntandomods-secret-2026-zimbabwe")

ADMIN_USERNAME = "ntandomods"
ADMIN_PASSWORD = "ntando"

STUDENT_BOOKS = [
    {"id":"book1","category":"short","title":"Till Operating Programme","subtitle":"2-Week Short Course","description":"Cash handling, EcoCash, bank transfers and card swipe — everything you need to operate a retail till confidently in Zimbabwe.","duration":"2 Weeks","fee_usd":35,"fee_zig":630,"badge":"SHORT COURSE","badge_color":"red","icon":"🏪","topics":["Cash Handling","EcoCash Payments","Bank Transfers","Card Swipe","Float Management","Till Balancing"],"pdf":"Book1-Till-Operating-Programme.pdf","docx":"Book1-Till-Operating-Programme.docx"},
    {"id":"book2","category":"diploma","title":"Computer Basics & Typing","subtitle":"Month 1 — 6-Month Diploma","description":"Fundamentals of using a computer, keyboard skills, and touch-typing from scratch.","duration":"1 Month","fee_usd":None,"fee_zig":None,"badge":"MONTH 1","badge_color":"blue","icon":"💻","topics":["Computer Hardware","Windows Basics","Keyboard Skills","Touch Typing","File Management","Basic Troubleshooting"],"pdf":"Book2-Month1-Computer-Basics-Typing.pdf","docx":"Book2-Month1-Computer-Basics-Typing.docx"},
    {"id":"book3","category":"diploma","title":"Microsoft Word","subtitle":"Month 2 — 6-Month Diploma","description":"Professional documents, CVs, letters and reports using Microsoft Word.","duration":"1 Month","fee_usd":None,"fee_zig":None,"badge":"MONTH 2","badge_color":"blue","icon":"📝","topics":["Formatting Text","Paragraphs & Styles","Tables","Mail Merge","CVs & Letters","Printing"],"pdf":"Book3-Month2-Microsoft-Word.pdf","docx":"Book3-Month2-Microsoft-Word.docx"},
    {"id":"book4","category":"diploma","title":"Microsoft Excel","subtitle":"Month 3 — 6-Month Diploma","description":"Spreadsheets, formulas, budgets, and data analysis for business and employment.","duration":"1 Month","fee_usd":None,"fee_zig":None,"badge":"MONTH 3","badge_color":"blue","icon":"📊","topics":["Spreadsheet Basics","Formulas & Functions","Charts & Graphs","Budget Templates","Data Sorting","Business Reports"],"pdf":"Book4-Month3-Microsoft-Excel.pdf","docx":"Book4-Month3-Microsoft-Excel.docx"},
    {"id":"book5","category":"diploma","title":"Microsoft PowerPoint","subtitle":"Month 4 — 6-Month Diploma","description":"Create professional presentations for business, school, and job applications.","duration":"1 Month","fee_usd":None,"fee_zig":None,"badge":"MONTH 4","badge_color":"blue","icon":"🎯","topics":["Slide Design","Transitions & Animations","Images & Charts","Speaker Notes","Business Presentations","Handouts"],"pdf":"Book5-Month4-Microsoft-PowerPoint.pdf","docx":"Book5-Month4-Microsoft-PowerPoint.docx"},
    {"id":"book6","category":"diploma","title":"Email & Internet","subtitle":"Month 5 — 6-Month Diploma","description":"Professional email, internet research, online safety and Google Drive.","duration":"1 Month","fee_usd":None,"fee_zig":None,"badge":"MONTH 5","badge_color":"blue","icon":"🌐","topics":["Gmail Setup","Professional Emails","Internet Research","Online Safety","Google Drive","Video Calls"],"pdf":"Book6-Month5-Email-Internet.pdf","docx":"Book6-Month5-Email-Internet.docx"},
    {"id":"book7","category":"diploma","title":"Social Media & Business","subtitle":"Month 6 — 6-Month Diploma","description":"Facebook, WhatsApp Business, TikTok and digital marketing for Zimbabwean entrepreneurs.","duration":"1 Month","fee_usd":None,"fee_zig":None,"badge":"MONTH 6","badge_color":"blue","icon":"📱","topics":["WhatsApp Business","Facebook Pages","TikTok for Business","Digital Marketing","Online Advertising","Brand Building"],"pdf":"Book7-Month6-Social-Media-Business.pdf","docx":"Book7-Month6-Social-Media-Business.docx"},
    {"id":"book8","category":"extra","title":"Basic Bookkeeping & Accounts","subtitle":"4-Week Course","description":"Cash books, ledgers, financial statements, VAT, ZIMRA obligations and Excel as a bookkeeping tool.","duration":"4 Weeks","fee_usd":45,"fee_zig":810,"badge":"4 WEEKS","badge_color":"purple","icon":"📒","topics":["Cash Book","Double Entry","Ledger Accounts","Income Statement","Balance Sheet","ZIMRA & VAT"],"pdf":"Book8-Bookkeeping-Accounts.pdf","docx":"Book8-Bookkeeping-Accounts.docx"},
    {"id":"book9","category":"extra","title":"Customer Service Excellence","subtitle":"2-Week Course","description":"First impressions, active listening, complaint handling and the GREAT Framework for Zimbabwean retail.","duration":"2 Weeks","fee_usd":30,"fee_zig":540,"badge":"2 WEEKS","badge_color":"green","icon":"🤝","topics":["GREAT Framework","Active Listening","Complaint Handling","De-escalation","Telephone Etiquette","Customer Retention"],"pdf":"Book9-Customer-Service-Excellence.pdf","docx":"Book9-Customer-Service-Excellence.docx"},
    {"id":"book10","category":"extra","title":"Data Entry & Office Administration","subtitle":"3-Week Course","description":"Touch typing (40+ WPM), filing systems, memos, databases, CSV data and remote work opportunities.","duration":"3 Weeks","fee_usd":35,"fee_zig":630,"badge":"3 WEEKS","badge_color":"orange","icon":"⌨️","topics":["Touch Typing","Numeric Keypad","Filing Systems","Office Reports","CSV & Databases","Remote Data Entry"],"pdf":"Book10-Data-Entry-Office-Admin.pdf","docx":"Book10-Data-Entry-Office-Admin.docx"},
    {"id":"book11","category":"extra","title":"Microsoft Office Professional","subtitle":"6-Week Course","description":"Deep mastery of Word, Excel, PowerPoint and Outlook with mail merge, VLOOKUP, PivotTables and business projects.","duration":"6 Weeks","fee_usd":55,"fee_zig":990,"badge":"6 WEEKS","badge_color":"blue","icon":"💻","topics":["Word Advanced","Excel Advanced","PowerPoint Pro","Mail Merge","VLOOKUP & PivotTables","Outlook & Calendar"],"pdf":"Book11-MS-Office-Professional.pdf","docx":"Book11-MS-Office-Professional.docx"},
    {"id":"book12","category":"extra","title":"Retail Management","subtitle":"8-Week Course","description":"Store operations, stock management, staff supervision, ZIMRA compliance and growing a retail business in Zimbabwe.","duration":"8 Weeks","fee_usd":70,"fee_zig":1260,"badge":"8 WEEKS","badge_color":"gold","icon":"🏪","topics":["Store Operations","Stock & Inventory","Staff Management","Loss Prevention","P&L for Managers","Sales Targets"],"pdf":"Book12-Retail-Management.pdf","docx":"Book12-Retail-Management.docx"},
    {"id":"book13","category":"extra","title":"Social Media Marketing","subtitle":"3-Week Course","description":"Facebook, Instagram, Canva, paid ads, content calendars, analytics built for Zimbabwean entrepreneurs.","duration":"3 Weeks","fee_usd":40,"fee_zig":720,"badge":"3 WEEKS","badge_color":"pink","icon":"📱","topics":["Facebook Business","Instagram Business","Canva Design","Content Strategy","Paid Ads","Analytics"],"pdf":"Book13-Social-Media-Marketing.pdf","docx":"Book13-Social-Media-Marketing.docx"},
    {"id":"book14","category":"extra","title":"Speed Typing & Computer Basics","subtitle":"1-Week Course","description":"Keyboard orientation, home row technique, accuracy drills — target 30 WPM in 5 days. Certificate issued same day.","duration":"1 Week","fee_usd":15,"fee_zig":270,"badge":"1 WEEK","badge_color":"teal","icon":"⌨️","topics":["Home Row Keys","Finger Placement","Speed Drills","Accuracy Training","Numeric Keypad","Same-Day Certificate"],"pdf":"Book14-Speed-Typing-Computer-Basics.pdf","docx":"Book14-Speed-Typing-Computer-Basics.docx"},
    {"id":"book15","category":"extra","title":"WhatsApp Business for Entrepreneurs","subtitle":"1-Week Course","description":"Product catalogue, broadcast marketing, labels, quick replies and EcoCash payment workflow for Zimbabwean SMEs.","duration":"1 Week","fee_usd":20,"fee_zig":360,"badge":"1 WEEK","badge_color":"green","icon":"💬","topics":["Business Profile Setup","Product Catalogue","Broadcast Lists","Quick Replies","EcoCash Workflow","WhatsApp API Overview"],"pdf":"Book15-WhatsApp-Business-Entrepreneurs.pdf","docx":"Book15-WhatsApp-Business-Entrepreneurs.docx"},
]

TEACHER_GUIDES = [
    {"id":"tg1","title":"Master Instructor Handbook","subtitle":"Complete Teacher Guide","description":"Full NtandoMods trainer handbook covering code of conduct, classroom management, lesson delivery and assessment.","icon":"👩‍🏫","pdf":"TeacherGuide1-Master-Instructor-Handbook.pdf","docx":"TeacherGuide1-Master-Instructor-Handbook.docx"},
    {"id":"tg2","title":"Bookkeeping Instructor Guide","subtitle":"Teacher Resource","description":"Lesson plans, worked examples and assessment rubrics for the Bookkeeping & Accounts course.","icon":"📒","pdf":"TeacherGuide2-Bookkeeping-Instructor.pdf","docx":"TeacherGuide2-Bookkeeping-Instructor.docx"},
    {"id":"tg3","title":"Social Media Marketing Instructor Guide","subtitle":"Teacher Resource","description":"Step-by-step lesson plans, live demo scripts and marking rubrics for the Social Media Marketing course.","icon":"📱","pdf":"TeacherGuide3-Social-Media-Instructor.pdf","docx":"TeacherGuide3-Social-Media-Instructor.docx"},
    {"id":"tg4","title":"Till Operating Instructor Guide","subtitle":"Teacher Resource","description":"Daily lesson plans, role-play scenarios and assessment criteria for the Till Operating Programme.","icon":"🏪","pdf":"TeacherGuide4-Till-Operating-Instructor.pdf","docx":"TeacherGuide4-Till-Operating-Instructor.docx"},
]

ADMIN_DOCS = [
    {"id":"ad1","title":"Student Registration Form","subtitle":"Admin Document","description":"Official NtandoMods student enrolment and registration form for all programmes.","icon":"📋","pdf":"Admin1-Student-Registration-Form.pdf","docx":"Admin1-Student-Registration-Form.docx"},
    {"id":"ad2","title":"Certificate Templates","subtitle":"Admin Document","description":"All NtandoMods certificate templates for every course and programme.","icon":"🏆","pdf":"Admin2-Certificate-Templates.pdf","docx":"Admin2-Certificate-Templates.docx"},
]

ALL_DOWNLOADABLE = {}
for lst in [STUDENT_BOOKS, TEACHER_GUIDES, ADMIN_DOCS]:
    for item in lst:
        ALL_DOWNLOADABLE[item["pdf"]] = "pdfs"
        ALL_DOWNLOADABLE[item["docx"]] = "docx"

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login", next=request.full_path))
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def index():
    return render_template("index.html",
        student_books=STUDENT_BOOKS,
        teacher_guides=TEACHER_GUIDES,
        admin_docs=ADMIN_DOCS,
        is_admin=session.get("admin_logged_in", False))

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()
        if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            next_url = request.args.get("next") or url_for("index")
            return redirect(next_url)
        error = "Incorrect username or password. Please try again."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/download/<filename>")
@login_required
def download(filename):
    if filename not in ALL_DOWNLOADABLE:
        abort(404)
    folder = ALL_DOWNLOADABLE[filename]
    mime = "application/pdf" if filename.endswith(".pdf") else \
           "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return send_from_directory(
        os.path.join(app.root_path, "static", folder),
        filename, as_attachment=True, mimetype=mime)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
