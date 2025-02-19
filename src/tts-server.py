import sys
import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from multiprocessing import Process, Queue
from tts.tts import generate_tts  # Updated import statement

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
    queue = Queue()
    try:
        process = Process(target=generate_tts, args=(text, speaker_wav, language, output_file, use_cuda, queue))
        process.start()
        process.join()
        result = queue.get()
        if result:
            with open(output_file, 'rb') as f:
                audio_content = f.read()
            return audio_content, 200
        else:
            return jsonify({'error': 'TTS generation failed.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

        queue = Queue()
        process = Process(target=generate_tts, args=(text, speaker_wav, language, output_file, use_cuda, queue))
        process.start()
        process.join()

        result = queue.get()
        if result:
            print(f"TTS generation completed: {result}")
        else:
            print("TTS generation failed.")