import tkinter as tk
from tkinter import filedialog, scrolledtext
import requests
import pdfplumber
import docx
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Flask server is running!"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


def extract_text_from_file(file_path):
    """Extract text from PDF or DOCX files."""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        text = ""  # Unsupported file type
    return text

def upload_resume():
    """Open file dialog to select a resume and extract its text."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    if file_path:
        extracted_text = extract_text_from_file(file_path)
        resume_entry.config(state=tk.NORMAL)
        resume_entry.delete("1.0", tk.END)
        resume_entry.insert(tk.END, extracted_text)
        resume_entry.config(state=tk.DISABLED)

def generate_resume():
    job_desc = job_desc_entry.get("1.0", tk.END).strip()
    experience = experience_entry.get("1.0", tk.END).strip()
    resume_text = resume_entry.get("1.0", tk.END).strip()

    if job_desc and experience and resume_text:
        response = requests.post("http://127.0.0.1:5000/generate", json={
            "job_description": job_desc,
            "experience": experience,
            "resume_text": resume_text
        })
        if response.status_code == 200:
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, response.json().get("generated_resume", "No response"))
            result_text.config(state=tk.DISABLED)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END, "Error generating resume.")
            result_text.config(state=tk.DISABLED)

# Tkinter UI Setup
root = tk.Tk()
root.title("AI Resume Builder")
root.geometry("600x600")

tk.Label(root, text="Job Description:").pack()
job_desc_entry = scrolledtext.ScrolledText(root, height=5, width=70)
job_desc_entry.pack()

tk.Label(root, text="Your Experience:").pack()
experience_entry = scrolledtext.ScrolledText(root, height=5, width=70)
experience_entry.pack()

upload_btn = tk.Button(root, text="Upload Resume", command=upload_resume)
upload_btn.pack()

tk.Label(root, text="Extracted Resume:").pack()
resume_entry = scrolledtext.ScrolledText(root, height=5, width=70, state=tk.DISABLED)
resume_entry.pack()

generate_btn = tk.Button(root, text="Generate Resume", command=generate_resume)
generate_btn.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=70, state=tk.DISABLED)
result_text.pack()

root.mainloop()

