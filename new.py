import gradio as gr
from models import groqai
from models import openai
from models import togetherai
from models import novitaai

def read_txt_file(txt_file):
    with open(txt_file.name, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def enable_buttons():
    return [gr.update(interactive=True) for _ in range(5)]

def perform_analysis(conversation, task_type):
    messages = {
        "customer_type": f"Classify the customer as 'Yangi' (new) or 'Eski' (old) based on the following conversation. Respond with either 'Yangi' or 'Eski'. \nConversation: {conversation}",
        "gender": f"Based on the conversation, classify the customer's GENDER: 'Erkak' (Male), 'Ayol' (Female), or 'Undefined'. Reply only with 'Erkak' or 'Ayol' or 'Undefined'. \nConversation: {conversation}",
        "sentiment": f"Analyze the sentiment of the job-related conversation and should be in UZBEK Language. Provide the response as follows: \nkayfiyat: ijobiy, salbiy, or neytral \nsabab: brief reason for this sentiment in uzbek. \nConversation: {conversation}",
        "main_topic": f"Identify the main topic of the call between the customer and staff in UZBEK Language. Respond with only the main topic. \nConversation: {conversation}",
        "summary": f"Provide a really short, clear, and detailed summary of the conversation in UZBEK Language! Keep your response under 3 sentences and just return the result. \nConversation: {conversation}"
    }
    
    return novitaai.generate_text(messages[task_type])

with gr.Blocks() as iface:
    txt_input = gr.File(type="filepath", label="Upload Text File (.txt)", file_types=[".txt"])
    text_output = gr.Textbox(label="Text from File")
    
    customer_type_output = gr.Textbox(label="Customer Type")
    gender_type_output = gr.Textbox(label="Gender")
    sentiment_output = gr.Textbox(label="Sentiment")
    topic_output = gr.Textbox(label="Main Topic")
    summary_output = gr.Textbox(label="Summary")
    
    read_button = gr.Button("Read Text File")
    customer_type_btn = gr.Button("Analyze Customer Type", interactive=False)
    gender_type_btn = gr.Button("Analyze Gender", interactive=False)
    sentiment_btn = gr.Button("Analyze Sentiment", interactive=False)
    topic_btn = gr.Button("Extract Main Topic", interactive=False)
    summary_btn = gr.Button("Summarize Call", interactive=False)
    
    read_button.click(
        read_txt_file,
        inputs=txt_input,
        outputs=text_output
    )
    
    text_output.change(
        enable_buttons,
        inputs=[],
        outputs=[customer_type_btn, gender_type_btn, sentiment_btn, topic_btn, summary_btn]
    )

    customer_type_btn.click(lambda conversation: perform_analysis(conversation, "customer_type"), inputs=text_output, outputs=customer_type_output)
    gender_type_btn.click(lambda conversation: perform_analysis(conversation, "gender"), inputs=text_output, outputs=gender_type_output)
    sentiment_btn.click(lambda conversation: perform_analysis(conversation, "sentiment"), inputs=text_output, outputs=sentiment_output)
    topic_btn.click(lambda conversation: perform_analysis(conversation, "main_topic"), inputs=text_output, outputs=topic_output)
    summary_btn.click(lambda conversation: perform_analysis(conversation, "summary"), inputs=text_output, outputs=summary_output)

iface.launch(share = False)