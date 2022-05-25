import os
import openai

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        response = openai.Completion.create(
            engine="text-curie-001",
            prompt=request.form.get("question"),
            temperature=0.5,
            top_p=1.0,
            max_tokens=64,
            echo=True,
        )
        return redirect(url_for("index", res=response.choices[0].text))
    result = request.values.get("res")
    return render_template('index.html', data=result)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)