import pdfplumber

def extract_text_from_pdf(pdf_file_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """
    with pdfplumber.open(pdf_file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

pdf_file_path = "database19c-wp.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path)
#print(extracted_text)

def sample_abstractive_summarization() -> None:
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
    key = "c644b0c375034d6fa81635d88ed89ead"

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    #extracted_text = "Your extracted text goes here..."

    print("Length before:", len(extracted_text))

    poller = text_analytics_client.begin_abstract_summary([extracted_text])
    for result in poller.result():
        if result.kind == "AbstractiveSummarization":
            print("Summarized:")
            for summary in result.summaries:
                print(summary.text)
                print("Length after:", len(summary.text))
        elif result.is_error:
            print(f"Error: {result.error.code}, {result.error.message}")

if __name__ == "__main__":
    sample_abstractive_summarization()

