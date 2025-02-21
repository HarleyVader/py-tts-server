import os
import logging
from flask import Flask, request, send_file, jsonify
import torch
from TTS.api import TTS
import threading
import time
import schedule
import re

# Set environment variable for CUDA launch blocking
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), 'audios')
os.makedirs(AUDIO_FOLDER, exist_ok=True)

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

    # Always use the bambi.wav file located in the same directory as the server
    speaker_wav = os.path.join(os.path.dirname(__file__), 'bambi.wav')
    language = data.get('language', 'en')
    
    # Check if speaker_wav file exists
    if not os.path.isfile(speaker_wav):
        return jsonify({"error": f"Speaker WAV file '{speaker_wav}' not found."}), 400
    
    # Clean the text to remove unwanted characters
    clean_text = re.sub(r'[,.?!\"*]', '', text)
    
    # Generate output filename based on cleaned text
    output_filename = '-'.join(clean_text.split()) + '.wav'
    output_path = os.path.join(AUDIO_FOLDER, output_filename)

    try:
        # Generate TTS
        tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=output_path)
        logging.info(f"TTS generated successfully: {output_path}")
    except torch.cuda.CudaError as e:
        logging.error(f"CUDA error: {e}")
        return jsonify({"error": f"CUDA error: {e}"}), 500
    except Exception as e:
        logging.error(f"Error generating TTS: {e}")
        return jsonify({"error": str(e)}), 500

    # Check if the output file was created
    if not os.path.isfile(output_path):
        logging.error(f"Output file not found: {output_path}")
        return jsonify({"error": "Output file not found."}), 500

    return send_file(output_path, as_attachment=True)

@app.route('/audios/<filename>')
def serve_audio(filename):
    file_path = os.path.join(AUDIO_FOLDER, filename)
    if not os.path.isfile(file_path):
        return jsonify({"error": "File not found."}), 404
    return send_file(file_path, as_attachment=True)

def garbage_collector():
    now = time.time()
    for filename in os.listdir(AUDIO_FOLDER):
        file_path = os.path.join(AUDIO_FOLDER, filename)
        if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > 600:
            os.remove(file_path)
            logging.info(f"Deleted old audio file: {file_path}")

def schedule_garbage_collector():
    schedule.every().day.at("06:00").do(garbage_collector)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=schedule_garbage_collector, daemon=True).start()
    port = int(os.getenv('TTS_PORT', 5002))
    app.run(host='0.0.0.0', port=port)