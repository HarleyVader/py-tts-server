import os
from flask import Flask, request, send_file
import torch
from TTS.api import TTS

app = Flask(__name__)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

@app.route('/tts', methods=['POST'])
def generate_tts():
    data = request.json
    text = data.get('text', 'Hello bambi!')
    speaker_wav = data.get('speaker_wav', './bambi.wav')
    language = data.get('language', 'en')
    
    # Generate output filename based on text
    output_filename = '-'.join(text.split()) + '.wav'
    output_path = output_filename

    # Generate TTS
    tts.tts_to_file(text=text, speaker_wav=speaker_wav, language=language, file_path=output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.getenv('TTS_PORT', 5002))
    app.run(host='0.0.0.0', port=port)