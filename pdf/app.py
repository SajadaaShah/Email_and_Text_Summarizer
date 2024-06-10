from flask import Flask, request, render_template
from pdfSummary import extract_text_from_pdf
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)

# Azure Text Analytics credentials
endpoint = "https://text-summarizer-sakshi.cognitiveservices.azure.com/"
key = "c644b0c375034d6fa81635d88ed89ead"
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize_pdf', methods=['POST'])
def summarize_pdf():
    if 'pdfFile' not in request.files:
        return 'No PDF file uploaded'
    
    pdf_file = request.files['pdfFile']
    if pdf_file.filename == '':
        return 'No PDF file selected'

    try:
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_file)
        
        # Generate summary using Azure Text Analytics
        poller = text_analytics_client.begin_abstract_summary([extracted_text])
        summary = ""
        for result in poller.result():
            if result.kind == "AbstractiveSummarization":
                for summary_obj in result.summaries:
                    summary += summary_obj.text
            elif result.is_error:
                return f"Error: {result.error.code}, {result.error.message}"
        
        return summary
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
