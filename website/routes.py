from datetime import datetime
from flask import Blueprint, render_template
from flask import request
from .models import Results
from openai import OpenAI

routes = Blueprint('routes', __name__)

client = OpenAI(
    api_key="Your-API-Key")

historyData = []
dataList = []


@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        query = request.args.get('query')
        if query == "" or query is None:
            return render_template('response_view.html')
        response = ask(query)
        queryMessage = Results(time=datetime.utcnow(), messagetype="other-message float-right", message=query)
        responseMessage = Results(time=datetime.utcnow(), messagetype="my-message", message=response)
        dataList.append(queryMessage)
        dataList.append(responseMessage)
        historyData.append(queryMessage)
        historyData.append(responseMessage)
        return render_template('response_view.html', results=dataList)
    else:
        return render_template('history.html', results=historyData)


def ask(question, chat_log=None):

    prompt = [
        {
            "role": "system",
            "content": ("You are a helpful assistant."),
        },
        {
            "role": "user",
            "content": (question),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=prompt, temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6,
        max_tokens=150)
    answer = response.choices[0].message.content.strip()
    return answer
