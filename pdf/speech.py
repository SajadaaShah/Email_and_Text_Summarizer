import pyttsx3

from pdfSummary import extract_text_from_pdf

def sample_abstractive_summarization_and_read_aloud() -> None:
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
    key = "c644b0c375034d6fa81635d88ed89ead"

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Extracted text
    extracted_text = extract_text_from_pdf("database19c-wp.pdf")

    print("Length before:", len(extracted_text))

    poller = text_analytics_client.begin_abstract_summary([extracted_text])
    for result in poller.result():
        if result.kind == "AbstractiveSummarization":
            print("Summarized:")
            summarized_text = ""
            for summary in result.summaries:
                summarized_text += summary.text
                print(summary.text)
                print("Length after:", len(summary.text))

            # Initialize the TTS engine
            engine = pyttsx3.init()

            # Set properties (optional)
            engine.setProperty('rate', 150)  # Speed of speech
            engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

            # Say the summarized text
            engine.say(summarized_text)
            engine.runAndWait()
        elif result.is_error:
            print(f"Error: {result.error.code}, {result.error.message}")

if __name__ == "__main__":
    sample_abstractive_summarization_and_read_aloud()