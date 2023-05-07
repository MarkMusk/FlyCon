from flask import Flask, render_template, request, redirect
from ai import generate
from metar import readMETAR, formatData

contentTo = None
contentFrom = None
warnings = None
opacities = None
result = None

app = Flask(__name__)

null = [None, '', ' ']

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    radio = request.args.get('radio')
    searchTo = request.args.get('to')
    searchFrom = request.args.get('from')
    deicing = request.args.get('deicing')
    print(f"RADIO= {radio}, SEARCH= {search} SWITCH= {deicing}")
    if searchTo not in null and searchFrom not in null:
        values = formatData(radio=radio, searchTo=searchTo, searchFrom=searchFrom, deicing=deicing)
        print(values)
        if not values:
            return render_template('error.html')
        if values == "NOMETAR":
            return render_template('nometar')
    else:
        return render_template('airesult.html', result='asdf')
    print(f"CONTENT TO: {values['contentTo']}")
    result = generate(prompt=f"What are some dangerous factors I should be aware of on a flight with: {values['contentTo']['metar']['cavok']}, wind speed {values['contentTo']['metar']['wind_speed']} kts")

    return render_template('search.html', contentTo=values['contentTo'], contentFrom=values['contentFrom'], warnings=values['warnings'], opacities=values['opacities'], result=result)

@app.route("/ai")
def searchAI():
    prompt = request.args.get('ai')
    print(f'PROMPT : {prompt}')
    if prompt == None:
        return render_template('ai.html')
    else:
        result = generate(prompt=prompt)
        return render_template('airesult.html', result=result, question=prompt)

@app.route("/how")
def howtouse():
    return render_template('how.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)