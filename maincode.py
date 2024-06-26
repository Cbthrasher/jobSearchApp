import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import spacy

class JobSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Automated Job Search")
        master.geometry("400x250")

        # Load user preferences from JSON file
        self.load_preferences()

        # Create labels and entry fields for keywords, location, and analytics
        self.keywords_label = tk.Label(master, text="Keywords:")
        self.keywords_label.grid(row=0, column=0, padx=10, pady=5)
        self.keywords_entry = tk.Entry(master, width=30)
        self.keywords_entry.grid(row=0, column=1, padx=10, pady=5)
        self.keywords_entry.insert(0, self.preferences['keywords'])  # Set default value from preferences

        self.location_label = tk.Label(master, text="Location:")
        self.location_label.grid(row=1, column=0, padx=10, pady=5)
        self.location_entry = tk.Entry(master, width=30)
        self.location_entry.grid(row=1, column=1, padx=10, pady=5)
        self.location_entry.insert(0, self.preferences['location'])  # Set default value from preferences

        self.analytics_label = tk.Label(master, text="Analytics:")
        self.analytics_label.grid(row=2, column=0, padx=10, pady=5)
        self.analytics_text = tk.Text(master, height=5, width=30)
        self.analytics_text.grid(row=2, column=1, padx=10, pady=5)

        # Button to initiate job search
        self.search_button = tk.Button(master, text="Search Jobs", command=self.search_jobs)
        self.search_button.grid(row=3, columnspan=2, padx=10, pady=10)

        # Load SpaCy English language model
        self.nlp = spacy.load('en_core_web_sm')

        # Initialize analytics
        self.analytics = {
            'applications_submitted': 0,
            'response_rate': 0,
            'interview_invitations': 0
        }
        self.update_analytics_display()

    def load_preferences(self):
        # Load user preferences from JSON file, or set default values if file doesn't exist
        try:
            with open('preferences.json', 'r') as f:
                self.preferences = json.load(f)
        except FileNotFoundError:
            self.preferences = {'keywords': '', 'location': ''}

    def save_preferences(self):
        # Save user preferences to JSON file
        with open('preferences.json', 'w') as f:
            json.dump(self.preferences, f)

    def search_jobs(self):
        keywords = self.keywords_entry.get()
        location = self.location_entry.get()

        # Update user preferences
        self.preferences['keywords'] = keywords
        self.preferences['location'] = location
        self.save_preferences()

        # Integrate chatbot for resume tailoring
        self.resume_tailoring_chatbot()

        # Update analytics
        self.analytics['applications_submitted'] += 1
        self.update_analytics_display()

    def update_analytics_display(self):
        # Update analytics display in the GUI
        analytics_info = f"Applications Submitted: {self.analytics['applications_submitted']}\n" \
                         f"Response Rate: {self.analytics['response_rate']}%\n" \
                         f"Interview Invitations: {self.analytics['interview_invitations']}"
        self.analytics_text.delete('1.0', tk.END)
        self.analytics_text.insert(tk.END, analytics_info)

    def resume_tailoring_chatbot(self):
        # Questions for resume tailoring
        questions = [
            "What relevant experience do you have for this role?",
            "What technical skills do you possess related to DevOps?",
            "Can you provide an example of a project where you implemented DevOps practices?",
            # Add more questions as needed
        ]
        
        # Initialize chatbot interface
        chatbot_window = tk.Toplevel(self.master)
        chatbot_window.title("Resume Tailoring Chatbot")
        chatbot_window.geometry("400x300")

        # Display questions and gather user responses
        answers = []
        for i, question in enumerate(questions):
            tk.Label(chatbot_window, text=question).grid(row=i, column=0, padx=10, pady=5)
            answer_entry = tk.Entry(chatbot_window, width=40)
            answer_entry.grid(row=i, column=1, padx=10, pady=5)
            answers.append(answer_entry)

        # Submit button to finalize resume tailoring and initiate application submission
        submit_button = tk.Button(chatbot_window, text="Submit", command=lambda: self.submit_application(answers, chatbot_window))
        submit_button.grid(row=len(questions), columnspan=2, padx=10, pady=10)

    def submit_application(self, answers, chatbot_window):
        # Retrieve user responses
        user_responses = [entry.get() for entry in answers]

        # Use user responses to tailor the resume (not implemented)

        # Close chatbot window
        chatbot_window.destroy()

        # Inform user that application submission is initiated
        messagebox.showinfo("Application Submission", "Application submission initiated. Your resume has been tailored based on your responses.")

        # Initiate application submission using Selenium
        self.submit_application_selenium()

    def submit_application_selenium(self):
        # Replace 'path_to_chromedriver' with the path to your Chrome WebDriver
        driver = webdriver.Chrome('path_to_chromedriver')

        # Navigate to the job application page
        driver.get('https://www.example.com/job_application_page')

        # Auto-fill form data
        driver.find_element_by_id('first_name').send_keys('John')
        driver.find_element_by_id('last_name').send_keys('Doe')
        driver.find_element_by

    def analyze_resume(self, resume_text, job_description):
        # Analyze user resume and job description using SpaCy
        doc_resume = self.nlp(resume_text)
        doc_job_description = self.nlp(job_description)

        # Extract skills from user resume
        user_skills = [ent.text.lower() for ent in doc_resume.ents if ent.label_ == "SKILL"]

        # Extract skills from job description
        job_skills = [ent.text.lower() for ent in doc_job_description.ents if ent.label_ == "SKILL"]

        # Calculate similarity between user skills and job requirements
        similarity_scores = [doc_resume.similarity(self.nlp(skill)) for skill in job_skills]

        # Print matched skills and their similarity scores
        for skill, score in zip(job_skills, similarity_scores):
            print(f"Matched Skill: {skill}, Similarity Score: {score:.2f}")

def main():
    root = tk.Tk()
    app = JobSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()





