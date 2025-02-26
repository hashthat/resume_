import tkinter as tk
from tkinter import scrolledtext
import requests

def generate_resume():
    job_desc = job_desc_entry.get("1.0", tk.END).strip()
    experience = experience_entry.get("1.0", tk.END).strip()
    if job_desc and experience:
        response = requests.post("http://127.0.0.1:5000/generate", json={
            "job_description": job_desc,
            "experience": experience
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
root.geometry("600x500")

tk.Label(root, text="Job Description:").pack()
job_desc_entry = scrolledtext.ScrolledText(root, height=5, width=70)
job_desc_entry.pack()

tk.Label(root, text="Your Experience:").pack()
experience_entry = scrolledtext.ScrolledText(root, height=5, width=70)
experience_entry.pack()

generate_btn = tk.Button(root, text="Generate Resume", command=generate_resume)
generate_btn.pack()

result_text = scrolledtext.ScrolledText(root, height=10, width=70, state=tk.DISABLED)
result_text.pack()

root.mainloop()
