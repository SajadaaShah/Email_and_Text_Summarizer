import time
import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def summarize_and_analyze_sentiment(email_threads, target_thread_ids, output_file):
    endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
    key = "c644b0c375034d6fa81635d88ed89ead"
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    counter = 0  # Initialize counter
    with open(output_file, 'w') as file:
        for target_thread_id in target_thread_ids:
            counter += 1  # Increment counter
            target_emails = [email for email in email_threads if email['thread_id'] == target_thread_id]
            sorted_emails = sorted(target_emails, key=lambda x: x['timestamp'])
            combined_body = ""

            for email in sorted_emails:
                body = email['body']
                sender = email['from']
                recipients = ", ".join(email['to'])
                combined_body += f"From: {sender}\nTo: {recipients}\n\n{body}\n\n"

            file.write(f"\nThread ID: {target_thread_id}\n")
            summarized_text = ""
            poller = text_analytics_client.begin_abstract_summary([combined_body])
            for result in poller.result():
                if result.kind == "AbstractiveSummarization":
                    for summary in result.summaries:
                        summarized_text += summary.text
                        file.write("Summarized Text:" + summary.text + "\n")
                elif result.is_error:
                    file.write(f"Error: {result.error.code}, {result.error.message}\n")

            # Add delay if counter is a multiple of 100, 200, 300, etc.
            if counter % 100 == 0:
                if counter % 300 == 0:
                    time.sleep(3)
                else:
                    time.sleep(2)

def get_unique_thread_ids(filename):
    with open(filename, 'r') as file:
        email_threads = json.load(file)
        unique_thread_ids = set()
        for email_thread in email_threads:
            unique_thread_ids.add(email_thread['thread_id'])
        return list(unique_thread_ids)

if __name__ == "__main__":
    # Load email threads from the JSON file
    with open("email_thread_reduced.json", 'r') as file:
        email_threads = json.load(file)

    # Get unique thread IDs
    target_thread_ids = get_unique_thread_ids("email_thread_details.json")

    # Define output file
    output_file = "summarized_threads.txt"

    # Call the summarization function
    summarize_and_analyze_sentiment(email_threads, target_thread_ids, output_file)
