import os
import logging
from flask import Flask, request, send_file, jsonify
import torch
from TTS.api import TTS

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

@app.route('/')
def index():
    return "Welcome to the TTS server. Use the /tts endpoint to generate speech."

@app.route('/tts', methods=['GET', 'POST'])
def generate_tts():
    if request.method == 'POST':
        data = request.json
    else:
        data = request.args

    text = data.get('text')
    if not text:
        return jsonify({"error": "Text parameter is required."}), 400

    speaker_wav = data.get('speaker_wav', './bambi.wav')
    language = data.get('language', 'en')
    
    # Check if speaker_wav file exists
    if not os.path.isfile(speaker_wav):
        return jsonify({"error": f"Speaker WAV file '{speaker_wav}' not found."}), 400
    
    # Generate output filename based on text
    output_filename = '-'.join(text.split()) + '.wav'
    output_path = output_filename

    try:
        # Generate TTS
        tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=output_path)
    except Exception as e:
        logging.error(f"Error generating TTS: {e}")
        return jsonify({"error": str(e)}), 500

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.getenv('TTS_PORT', 5002))
    app.run(host='0.0.0.0', port=port)