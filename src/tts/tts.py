import sys
import os
import logging
from dotenv import load_dotenv
from TTS.api import TTS  # Import Coqui TTS
from multiprocessing import Process, Queue

def generate_tts(text, speaker_wav, language, output_file, use_cuda, queue=None):
    print(f"[TTS SCRIPT] Generating TTS for text='{text}', speaker_wav='{speaker_wav}', language='{language}', output_file='{output_file}', use_cuda={use_cuda}")
    # Initialize TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=use_cuda)
    try:
        # Generate TTS
        tts.tts_to_file(text=text, file_path=output_file)
        print(f"[TTS SCRIPT] TTS generation successful, output file: {output_file}")
        if queue:
            queue.put(output_file)
    except Exception as e:
        print(f"[TTS SCRIPT] Error during TTS generation: {str(e)}")
        if queue:
            queue.put(None)
        raise

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python tts.py <text> <speaker_wav> <language> <output_file> <use_cuda>")
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
        print(f"[TTS SCRIPT] TTS generation completed: {result}")
    else:
        print("[TTS SCRIPT] TTS generation failed.")
