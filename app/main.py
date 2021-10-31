import en_core_web_sm
nlp = en_core_web_sm.load()
import os
PEOPLE_FOLDER = os.path.join('static/img/bg.jpg')
import chatterbot
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter",logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'],
        database_uri='sqlite:///database.sqlite3'
    )
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")
trainer = ListTrainer(english_bot)
trainer.train("./vatly.yml")



@app.route("/")
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bg.jpg')
    return render_template("index.html", user_image = full_filename)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))
    return str()


if __name__ == "__main__":
    import webbrowser
    webbrowser.open_new_tab('http://127.0.0.1:5000')
    app.run()