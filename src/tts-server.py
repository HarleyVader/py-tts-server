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
    use_cuda = data.get('use_cuda', True)  # Default to True if not provided

    print(f"[TTS SERVER] Received request with text={text}, speaker_wav={speaker_wav}, language={language}, use_cuda={use_cuda}")

    if not text or not speaker_wav or not language:
        print("[TTS SERVER] Missing required parameters")
        return jsonify({'error': 'Missing required parameters'}), 400

    output_file = f"output/{speaker_wav}_{language}_{text[:10]}.wav"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        command = [
            "python", "./src/tts.py",
            text, speaker_wav, language, output_file, str(use_cuda)
        ]
        print(f"[TTS SERVER] Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[TTS SERVER] Command failed with error: {result.stderr}")
            raise Exception(result.stderr)
        print(f"[TTS SERVER] Command succeeded, output file: {output_file}")
        return jsonify({'audio_file': output_file}), 200
    except Exception as e:
        print(f"[TTS SERVER] Exception occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)