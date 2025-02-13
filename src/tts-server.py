from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/generate-tts', methods=['POST'])
def generate_tts_route():
    data = request.json
    text = data.get('text')
    speaker_wav = data.get('speaker')
    language = data.get('language')

    if not text or not speaker_wav or not language:
        return jsonify({'error': 'Missing required parameters'}), 400

    output_file = f"output/{speaker_wav}_{language}_{text[:10]}.wav"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        command = [
            "python", "/mnt/f/js-bambisleep-chat-MK-VIII/workers/python/tts.py",
            text, speaker_wav, language, output_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        return jsonify({'audio_file': output_file}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)