import json

# Load JSON data from file
with open("email_thread_details.json", 'r') as file:
    email_threads = json.load(file)

# Specify the thread ID you're interested in
target_thread_id = 1

# Filter emails belonging to the specified thread ID
target_emails = [email for email in email_threads if email['thread_id'] == target_thread_id]

# Sort emails by timestamp
sorted_emails = sorted(target_emails, key=lambda x: x['timestamp'])

# Initialize an empty string to store the combined body content
combined_body = ""

# Iterate over each email in the sorted list
for email in sorted_emails:
    body = email['body']
    sender = email['from']
    recipients = ", ".join(email['to'])

    # Append email details and body content to the combined string
    combined_body += f"From: {sender}\nTo: {recipients}\n\n{body}\n\n"

# Print or use the combined body content for the specified thread
#print(combined_body)


from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def sample_abstractive_summarization() -> None:
    endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
    key = "c644b0c375034d6fa81635d88ed89ead"

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = text_analytics_client.begin_abstract_summary([combined_body])
    sum1 = ""  # Initialize sum1
    for result in poller.result():
        if result.kind == "AbstractiveSummarization":
            print("Summarized:")
            for summary in result.summaries:
                sum1 += summary.text  # Append summary text to sum1
                print(summary.text)  # Print summary text
        elif result.is_error:
            print(f"Error: {result.error.code}, {result.error.message}")

    return sum1  # Return the summarized text


from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Replace with your Cognitive Services endpoint and key
endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
key = "c644b0c375034d6fa81635d88ed89ead"

def analyze_sentiment(text):
    credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    response = text_analytics_client.analyze_sentiment(documents=[{"id": "1", "text": text}])
    for document in response:
        # print("Text: ", document['id'])
        print("Sentiment: ", document['sentiment'])
        # print("Confidence Scores: ")
        # print("\tPositive: {:.2f}".format(document['confidence_scores']['positive']))
        # print("\tNeutral: {:.2f}".format(document['confidence_scores']['neutral']))
        # print("\tNegative: {:.2f}".format(document['confidence_scores']['negative']))
        print()


if __name__ == "__main__":
    sum1 = sample_abstractive_summarization()
    analyze_sentiment(sum1)