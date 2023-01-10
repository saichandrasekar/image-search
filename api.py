from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    #return "<p>Hello, World!</p>"
    return render_template('inputs.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('./test-files/'+uploaded_file.txt')