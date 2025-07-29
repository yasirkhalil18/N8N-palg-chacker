from flask import Flask, request, jsonify
from plagiarism_checker import check_plagiarism

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'Text is required.'}), 400
        result = check_plagiarism(text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
