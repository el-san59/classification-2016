from flask import Flask, request, render_template
from query import find_query
from classifier import get_tag
from sklearn.externals import joblib

model = joblib.load('svc.model')
tfidf = joblib.load('tfidf.model')

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)


@app.route('/')
@app.route('/search')
def hello():
    return render_template('search.html')

@app.route('/define')
def hello2():
    return render_template('define.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_request = request.form['request']
        entries = find_query(search_request)
        return render_template('search_results.html', search_request=search_request, entries=entries)


@app.route('/define', methods=['GET', 'POST'])
def define():
    if request.method == 'POST':
        text = request.form['text']
        entries = get_tag(text, model, tfidf)
        return render_template('define_type.html', text=text, entries=entries)


if __name__ == '__main__':
    app.run(debug=True)
