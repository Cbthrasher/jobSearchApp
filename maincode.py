import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import requests
from bs4 import BeautifulSoup

def main():
    root = tk.Tk()
    app = JobSearchApp(root)
    root.mainloop()

class JobSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Automated Job Search")
        master.geometry("400x200")

        # Load user preferences from JSON file
        self.load_preferences()

        # Create labels and entry fields for keywords and location
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

        # Button to initiate job search
        self.search_button = tk.Button(master, text="Search Jobs", command=self.search_jobs)
        self.search_button.grid(row=2, columnspan=2, padx=10, pady=10)

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

        # Retrieve job listings
        job_listings = self.retrieve_job_listings(keywords, location)

        # Display job listings
        self.display_job_listings(job_listings)

    def retrieve_job_listings(self, keywords, location):
        url = f'https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = []

        listings = soup.find_all('li', class_='result-card')
        for listing in listings:
            title = listing.find('h3').text.strip()
            company = listing.find('h4').text.strip()
            location = listing.find('span', class_='job-result-card__location').text.strip()
            job_listings.append({'title': title, 'company': company, 'location': location})

        return job_listings

    def display_job_listings(self, job_listings):
        # Display job listings in the GUI
        if job_listings:
            messagebox.showinfo("Job Listings", "\n".join([f"{job['title']} - {job['company']} - {job['location']}" for job in job_listings]))
        else:
            messagebox.showinfo("Job Listings", "No job listings found.")

if __name__ == "__main__":
    main()
