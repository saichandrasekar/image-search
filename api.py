# Runs as : flask --app api run --host=0.0.0.0


from flask import Flask, render_template, request, send_file
import time as time_

from service import init_search_repo, search_image_repo

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
        f.save('./test-image/' + new_file_name)

        response = {
            'status': 'success',
            'fileName': new_file_name
        }
        return render_template('search.html', response=new_file_name)


@app.route("/search", methods=['GET'])
def search_image():
    test_image_name = request.args.get('test-file-name', '')

    print("Test Image Name:",test_image_name)

    result_image = search_image_repo(test_image_name)
    if result_image is not None:
        return send_file(result_image, mimetype='image/jpeg')
    else:
        return render_template('result-404.html'), 404
