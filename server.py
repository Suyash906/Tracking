from flask import Flask, url_for, send_from_directory, request
import logging, os
from werkzeug.utils import secure_filename
from flask import jsonify, make_response
# import worker
import grpc_client

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ['POST'])
def api_root():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:
        app.logger.info(app.config['UPLOAD_FOLDER'])
        img = request.files['image']
        img_name = secure_filename(img.filename)
        client = grpc_client.Client('localhost:9999')
        client.upload(img, img_name)
        # create_new_folder(app.config['UPLOAD_FOLDER'])
        # saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        # app.logger.info("saving {}".format(saved_path))
        # img.save(saved_path)
        # worker.enqueue_request_queue(img.filename,"write")
        # worker.blockThread()
        # return make_response(jsonify({"success":True,"filename":img.filename}),200)
        return make_response(jsonify({"success":True}),200)
    else:
        return "Where is the file?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)