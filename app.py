from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if image_file:
        result = process_with_model(image_file)
        return jsonify({'result': result})

def process_with_model(image_file):
    return "Thinking..."

if __name__ == '__main__':
    app.run(debug=True)
