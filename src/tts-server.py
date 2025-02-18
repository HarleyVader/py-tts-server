import sys
import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/tts', methods=['POST'])
def tts_endpoint():
    data = request.get_json()
    text = data['text']
    speaker_wav = data['speaker_wav']
    language = data['language']
    output_file = data['output_file']
    use_cuda = data['use_cuda']
    try:
        generate_tts(text, speaker_wav, language, output_file, use_cuda)
        with open(output_file, 'rb') as f:
            audio_content = f.read()
        return audio_content, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_tts(text, speaker_wav, language, output_file, use_cuda):
    print(f"[TTS SCRIPT] Generating TTS for text='{text}', speaker_wav='{speaker_wav}', language='{language}', output_file='{output_file}', use_cuda={use_cuda}")
    # Simulate TTS generation process
    try:
        # Your TTS generation logic here
        with open(output_file, 'w') as f:
            f.write("Simulated TTS audio content")
        print(f"[TTS SCRIPT] TTS generation successful, output file: {output_file}")
    except Exception as e:
        print(f"[TTS SCRIPT] Error during TTS generation: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'serve':
        app.run(host='0.0.0.0', port=5002)
    else:
        if len(sys.argv) < 6:
            print("Usage: python tts-server.py <text> <speaker_wav> <language> <output_file> <use_cuda>")
            sys.exit(1)

        text = sys.argv[1]
        speaker_wav = sys.argv[2]
        language = sys.argv[3]
        output_file = sys.argv[4]
        use_cuda = sys.argv[5].lower() == 'true'

        generate_tts(text, speaker_wav, language, output_file, use_cuda)