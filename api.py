# Runs as : flask --app api run --host=0.0.0.0


from flask import Flask, render_template, request, send_file
import time as time_

from service import init_search_repo

app = Flask(__name__)
init_search_repo()


@app.route("/")
def hello_world():
    return render_template('inputs.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['input_image']
        new_file_name = str(round(time_.time() * 1000)) + '_' + f.filename

        print("New file Name :", new_file_name)
        f.save('./../test_files/' + new_file_name)

        response = {
            'status': 'success',
            'fileName': new_file_name
        }
        return render_template('search.html', response=new_file_name)


@app.route("/search", methods=['GET'])
def search_image():
    return render_template('result.html')
