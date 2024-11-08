import gradio as gr
from uzbekvoice import transcription
from punctuation import punctuations
from models import groqai
from models import openai
from models import novitaai
from models import togetherai

def transcribe_audio(audio_path):
    original_text = transcription(audio_path)
    punctuated_text = punctuations(original_text)
    return original_text, punctuated_text, True

def enable_buttons():
    # Enable all buttons after transcription is complete
    return [gr.update(interactive=True) for _ in range(5)]

def perform_analysis(conversation, task_type):
    # Define messages for each task
    messages = {
        "customer_type": f"Classify the customer as 'Yangi' (new) or 'Eski' (old) based on the following conversation. Respond with either 'Yangi' or 'Eski'. \nConversation: {conversation}",
        "gender": f"Based on the conversation, classify the customer's gender. Reply only with 'Erkak', 'Ayol', or 'Undefined'. \nConversation: {conversation}",
        "sentiment": f"Analyze the sentiment of the job-related conversation and should be in UZBEK Language. Provide the response as follows: \nkayfiyat: ijobiy, salbiy, or neytral \nsabab: brief reason for this sentiment in uzbek. \nConversation: {conversation}",
        "main_topic": f"Identify the main topic of the call between the customer and staff in UZBEK Language. Respond with only the main topic. \nConversation: {conversation}",
        "summary": f"Provide a really short, clear, and detailed summary of the conversation in UZBEK Language! Keep your response under 3 sentences and just return the result. \nConversation: {conversation}"
    }

    # return openai.generate_text(messages[task_type])
    return groqai.generate_text(messages[task_type])

# Gradio interface
with gr.Blocks() as iface:
    audio_input = gr.Audio(type="filepath", label="Upload or record audio")
    transcribed_text = gr.State("")
    transcription_complete = gr.State(False)
    
    transcribe_button = gr.Button("Transcribe Audio")
    
    original_text_output = gr.Textbox(label="Transcription without Punctuation")
    punctuated_text_output = gr.Textbox(label="Transcription with Punctuation")
    
    customer_type_output = gr.Textbox(label="Customer Type")
    gender_type_output = gr.Textbox(label="Gender")
    sentiment_output = gr.Textbox(label="Sentiment")
    topic_output = gr.Textbox(label="Main Topic")
    summary_output = gr.Textbox(label="Summary")
    
    customer_type_btn = gr.Button("Analyze Customer Type", interactive=False)
    gender_type_btn = gr.Button("Analyze Gender", interactive=False)
    sentiment_btn = gr.Button("Analyze Sentiment", interactive=False)
    topic_btn = gr.Button("Extract Main Topic", interactive=False)
    summary_btn = gr.Button("Summarize Call", interactive=False)
    
    transcribe_button.click(
        transcribe_audio,
        inputs=audio_input,
        outputs=[original_text_output, punctuated_text_output, transcription_complete]
    )
    
    # Enable analysis buttons once transcription is done
    punctuated_text_output.change(
        enable_buttons,
        inputs=[],
        outputs=[customer_type_btn, gender_type_btn, sentiment_btn, topic_btn, summary_btn]
    )

    # Define button click actions using the consolidated function
    customer_type_btn.click(lambda conversation: perform_analysis(conversation, "customer_type"), inputs=punctuated_text_output, outputs=customer_type_output)
    gender_type_btn.click(lambda conversation: perform_analysis(conversation, "gender"), inputs=punctuated_text_output, outputs=gender_type_output)
    sentiment_btn.click(lambda conversation: perform_analysis(conversation, "sentiment"), inputs=punctuated_text_output, outputs=sentiment_output)
    topic_btn.click(lambda conversation: perform_analysis(conversation, "main_topic"), inputs=punctuated_text_output, outputs=topic_output)
    summary_btn.click(lambda conversation: perform_analysis(conversation, "summary"), inputs=punctuated_text_output, outputs=summary_output)

iface.launch(share=True)
