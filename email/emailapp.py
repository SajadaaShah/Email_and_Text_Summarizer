from flask import Flask, request, render_template, jsonify
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Initialize Flask app
app = Flask(__name__)

# Load email thread details from JSON file
with open("email_thread_details.json", 'r') as file:
    email_threads = json.load(file)

# Define function to generate summary based on thread ID
def generate_summary(thread_id):
    target_emails = [email for email in email_threads if email['thread_id'] == thread_id]
    combined_body = ""
    for email in target_emails:
        combined_body += email['body'] + "\n\n"
    return combined_body

# Define function to perform abstractive summarization using Azure Text Analytics
def generate_abstractive_summary(text):
    endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
    key = "c644b0c375034d6fa81635d88ed89ead"
    credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    poller = text_analytics_client.begin_abstract_summary([text])
    summarized_text = ""
    for result in poller.result():
        if result.kind == "AbstractiveSummarization":
            for summary in result.summaries:
                summarized_text += summary.text
        elif result.is_error:
            print(f"Error: {result.error.code}, {result.error.message}")
    return summarized_text

# Define route to render the HTML form
@app.route('/')
def index():
    return render_template('email.html', email_threads=email_threads)

# Define route to handle form submission and generate summary
@app.route('/generate_email_summary', methods=['POST'])
def generate_email_summary():
    thread_id = int(request.form['threadId'])  # Get thread ID from form submission
    summary = generate_summary(thread_id)  # Generate summary based on thread ID
    abstractive_summary = generate_abstractive_summary(summary)  # Generate abstractive summary
    return jsonify({'summary': abstractive_summary})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
