# 🗣️ Voice Chatbot

A fully functional **AI-powered voice chatbot** that listens to user queries, processes them using **Groq API (ChatGPT-based LLM), Faster Whisper (speech-to-text), and Parler-TTS (text-to-speech)**, and responds in a human-like voice.

## 🌟 Features

- 🎙️ **Speech-to-Text** using Faster Whisper for high-speed, low-latency transcription
- 🤖 **AI-Powered Response** using the Groq API (ChatGPT-based model)
- 🔊 **Text-to-Speech** using Parler-TTS to generate realistic human-like responses
- 🏗️ **REST API** built with FastAPI for backend processing
- 🎨 **Interactive Frontend** built with React for easy interaction
- 🌍 **Fully Remote Deployment** - Run anywhere with Python & Node.js

## 🏗️ Project Structure

```
voice-chatbot
├── backend/                # Backend API
│   ├── app/
│   │   ├── api.py          # FastAPI-based API router
│   │   ├── llm_response.py # Handles LLM query processing
│   │   ├── speech_to_text.py # Converts voice input to text
│   │   ├── text_to_speech.py # Converts AI response to speech
│   ├── core/
│   │   ├── config.py       # Configuration file (API keys, etc.)
│   ├── audio_inputs/       # Stores recorded user audio
│   ├── audio_outputs/      # Stores generated AI audio responses
│   ├── requirements.txt    # Python dependencies
│   ├── main.py             # Connects all components
├── frontend/               # Frontend UI (React)
│   ├── public/
│   ├── src/
│   │   ├── pages/          # UI components
│   │   ├── App.tsx         # Main React app
│   │   ├── index.tsx       # React entry point
│   ├── package.json        # Frontend dependencies
│   ├── README.md           # Frontend-specific docs
├── .gitignore              # Ignore unnecessary files
├── README.md               # Project documentation
```

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/process_text/` | Process text input and generate speech response |
| POST | `/process_audio_file/` | Upload and process audio file |
| POST | `/process_mic/` | Process real-time microphone input |

### Endpoint Details

#### 1. Text Input Endpoint (`/process_text/`)
- **Method**: POST
- **Description**: Converts text input to an AI-generated response with audio output
- **Request Body**: 
  ```json
  {
    "text": "Your input text here"
  }
  ```
- **Response**: 
  - `Input Text`: Original input text
  - `LLM Response`: AI-generated response
  - `Audio`: Base64 encoded audio file
  - `Audio Path`: Path to saved audio file

#### 2. Audio File Input Endpoint (`/process_audio_file/`)
- **Method**: POST
- **Description**: Uploads an audio file, transcribes it, generates an AI response, and creates an audio response
- **Request Body**: Multipart form-data with audio file
- **Response**: 
  - `Transcription`: Transcribed text from audio
  - `LLM Response`: AI-generated response
  - `Audio`: Base64 encoded audio file
  - `Audio Path`: Path to saved audio file

#### 3. Real-Time Microphone Input Endpoint (`/process_mic/`)
- **Method**: POST
- **Description**: Processes real-time microphone input, generates AI response with audio output
- **Request Body**: None
- **Response**: 
  - `Transcription`: Transcribed text from microphone
  - `LLM Response`: AI-generated response
  - `Audio`: Base64 encoded audio file
  - `Audio Path`: Path to saved audio file

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Gangatharangurusamy/voice-ai-chatbot.git
cd voice-chatbot
```

### 2. Setup Backend (Conda & Python)

#### Create Conda Environment

```bash
# Create a new Conda environment with Python 3.10
conda create -p env-voice-chatbot python=3.10

# Activate the environment
conda activate env-voice-chatbot/

# Install dependencies
cd backend
pip install -r requirements.txt
```

#### Set Up Environment Variables

Create a `.env` file inside `backend/` and add:

```ini
GROQ_API_KEY=your_groq_api_key
WHISPER_MODEL=large-v3
```

#### Run the Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Setup Frontend (React & TypeScript)

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Run the Frontend

```bash
npm start
```

Your app will now be running at `http://localhost:3000` 🎉

### 4. Deactivate Environment (When Done)

```bash
conda deactivate
```

#### Set Up Environment Variables

Create a `.env` file inside `backend/` and add:

```ini
GROQ_API_KEY=your_groq_api_key
```

#### Run the Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔍 Design Decisions

### Faster Whisper for STT
- Chosen for high accuracy and faster inference compared to OpenAI Whisper
- Runs efficiently on CPU/GPU with optimized faster-whisper package

### Groq API for AI Responses
- Provides ChatGPT-level responses at lower cost & latency
- Easily integrates into FastAPI

### Parler-TTS for Speech Generation
- Chosen for realistic, human-like voice output
- Supports custom tunable parameters like pitch, speed, and voice type

### FastAPI for Backend
- Used for lightweight & high-speed API routing
- Allows easy scalability & containerization (Docker support)

### React for Frontend
- Provides an interactive UI for users to chat with the bot
- Uses TypeScript for better maintainability

## 🛠️ Challenges & Learnings

### 🔴 Challenges
- Latency Issues: Initial audio generation was slow. Optimized with half-precision models
- Noise Handling: Improved STT accuracy by using VadFilter for noise reduction
- API Rate Limits: Managed by caching responses when possible

### ✅ Key Improvements
- Optimized Faster Whisper parameters to reduce CPU/GPU usage
- Enabled batch processing for real-time voice responses
- Improved UI design for a seamless user experience

## 🎯 Future Enhancements
- 🏗 Fine-tune Parler-TTS for even better voice customization
- 🎭 Personalized AI Responses based on user history
- 🌐 Deploy on Cloud (AWS/GCP) for scalable performance

## 💡 How to Contribute
We welcome contributions! Please fork the repo, create a branch, and submit a PR. 🚀

## 📜 License
MIT License - Feel free to modify and use this project.