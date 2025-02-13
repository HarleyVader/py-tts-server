# Coqui TTS Server

This project is a server application that utilizes the Coqui TTS Python API to generate text-to-speech (TTS) audio files. It is built using Flask and provides a simple interface for generating speech from text.

## Project Structure

```
coqui-tts-server
├── src
│   ├── app.py                # Main entry point of the server application
│   ├── tts
│   │   └── generate_tts.py   # Function to generate TTS using Coqui TTS API
│   └── utils
│       └── __init__.py       # Utility functions and classes
├── requirements.txt           # Project dependencies
├── Dockerfile                  # Instructions to build the Docker image
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd coqui-tts-server
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the server:**
   ```
   python src/app.py
   ```

2. **Make a request to generate TTS:**
   You can use tools like `curl` or Postman to send a POST request to the server with the text, speaker, and language parameters.

   Example request:
   ```
   POST /generate_tts
   {
       "text": "Hello, world!",
       "speaker": "en",
       "language": "en"
   }
   ```

## Docker

To build and run the application using Docker, follow these steps:

1. **Build the Docker image:**
   ```
   docker build -t coqui-tts-server .
   ```

2. **Run the Docker container:**
   ```
   docker run -p 5000:5000 coqui-tts-server
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.