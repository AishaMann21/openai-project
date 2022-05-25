import os
import openai

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form.get("question")
        response = openai.Completion.create(
            engine="text-curie-001",
            prompt= generate_prompt(question),
            temperature=0.5,
            top_p=1.0,
            max_tokens=64,
        )
        return redirect(url_for("index", res=response.choices[0].text))
    result = request.values.get("res")
    return render_template('index.html', data=result)

def generate_prompt(question):
    return """ I am a highly intelligent question answering bot. I only answer questions about characters in Marvel Cinematic Universe, Marvel Comics, DC Comics, All Star Comics and DC Extended Universe. If you ask me anything else, I will respond with "I don't know how to answer that".
question: Is Wanda Maximoff Evil?
answer: Wanda Maximoff went evil in Doctor Strange to reunite with her children after losing them in WandaVision
question: Who is the strongest Avenger?
answer: Some say it's Hulk because of his strength and some say it's Scarlet Witch because of the Dark Hold. But there is no definitive answer.
question: What are Wanda's powers?
answer: Wanda's abilities include telekinesis, energy manipulation, and some form of neuroelectric interfacing that allows her to both read thoughts and also give her targets waking nightmares.
question: How to make eggs?
answer: I don't know how to answer that.
question: Is DC better than Marvel?
answer: I don't know how to answer that.
question: {}
answer:""".format(question.capitalize())

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)