'''
File: app.py
Project: ChatUSGS
File Created: 17 March 2023 9:47:20 am
Author: Perry Oddo (perry.oddo@nasa.gov)
-----
Last Modified: 17 April 2023 2:12:27 pm
Modified By: Perry Oddo (perry.oddo@nasa.gov>)
-----
Description: Simple Gradio chat interface for GPT-3.5 NLP Data Access using USGS Graph Image API
'''

import gradio as gr
from backend import submit_prompt

def add_text(history, text):
    history = history + [(text, None)]
    return history, ""

def welcome():
    message = "Hello, what data can I help you find?"
    return message

def get_graph(text):
    output = submit_prompt(text)
    graph = output[1]
    return graph

def bot(history):
    response = "Let's find that data for you!"
    history[-1][1] = response
    return history

with gr.Blocks(theme=gr.themes.Soft(), title="NLP Data Access") as app:
    gr.Markdown("# NLP Data Access using GPT-3.5")
    with gr.Row().style(equal_height=True):
        with gr.Column(scale=0.35):
            chat = gr.Chatbot([], elem_id="chatbot").style(height=525)
        with gr.Column(scale=0.65):
            window = gr.Image().style(height=550)
    with gr.Row(variant="compact"):
        text = gr.Textbox(
            label="Enter your prompt",
            show_label=False,
            max_lines=1,
            placeholder="Enter your prompt",
        ).style(
            container=False,
        )
        btn = gr.Button("Get data").style(full_width=False)

    btn.click(get_graph, [text], window)
    text.submit(get_graph, [text], window)

    text.submit(add_text, [chat, text], [chat, text]).then(
        bot, chat, chat
    )
    
    btn.click(lambda x: gr.update(value=""), [], [text])
    text.submit(lambda x: gr.update(value=""), [], [text])

app.launch(favicon_path="img/nasa.png")