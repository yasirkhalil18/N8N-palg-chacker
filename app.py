from flask import Flask, request, jsonify
from plagiarism_checker import check_text  # Make sure this function exists

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    percent = check_text(text)  # Should return a percentage as float/int
    return jsonify({'plag_percent': percent})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
