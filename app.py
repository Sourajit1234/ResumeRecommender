import os
import csv
import lmstudio as lms
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pdfplumber
## DISPLAY ACCURACY
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'resumes_data.csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders and CSV exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header row for the CSV
        writer.writerow(["Name", "Email", "Skills", "Summary", "Job Titles", "Advice"])


def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text


def get_ai_data(full_text):
    # Get the model handle
    model = lms.llm("qwen/qwen3-vl-4b")

    # Initialize chat with your specific prompt and the extracted text
    system_prompt = (
            "You are a resume data extractor and professional career advisor. "
            "You answer concisely and do not use any other words than asked."
            "If something is not available in the resume, return 'NaN', do not assume things."
            "Extract the name verbatim. Do not change the spelling."
            "You extract information from the given text: " + full_text
    )
    chat = lms.Chat(system_prompt)

    def ask(question):
        chat.add_user_message(question)
        # Fix: Access the .content attribute and use on_message to update history
        response = model.respond(chat, on_message=chat.append)
        return response.content.strip()

    # Sequential extractions
    name = ask("The candidate's full name, without changing the spelling.")
    email = ask("Contact email address")
    skills = ask("List of key technical skills found")
    summary = ask("A 2-sentence summary of work history")
    titles = ask("Top 3 job titles they should apply for")
    advice = ask("Give the full career advice along with immediate next step (ex. college, job etc): ")

    return [name, email, skills, summary, titles, advice]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            # 1. Save the file temporarily
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # 2. Extract text and get AI analysis
            text = extract_text_from_pdf(file_path)
            data = get_ai_data(text)

            # 3. Store in CSV
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)

            # 4. Render results (Advice and Name)
            return render_template('index.html',
                                   advice=data[5],
                                   name=data[0],
                                   success=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)