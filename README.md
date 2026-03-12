# 🕷️ Spider AI — Personal AI Desktop Assistant

<p align="center">
  <img src="Frontend/Graphics/spider.gif" alt="Spider AI" width="480"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cohere-Command_XL-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge&logo=qt" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

---

## 📖 About

**Spider AI** is a fully featured AI-powered desktop assistant for Windows. It combines voice recognition, text-to-speech, real-time web search, AI chat, image generation, and system automation — all wrapped in a sleek, dark-themed **PyQt5 GUI**. Inspired by Jarvis-style assistants, Spider AI acts as your personal productivity companion that understands and executes natural language commands.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎤 **Voice Recognition** | Microphone-based speech input via Selenium + Web Speech API |
| 🔊 **Text-to-Speech** | Realistic voice output using Microsoft Edge TTS + Pygame |
| 🤖 **AI Chatbot** | Context-aware conversations powered by Groq (LLaMA 3.1 8B) |
| 🌐 **Real-Time Search** | Live web answers via Google Search + Groq (LLaMA 3.1 8B) |
| 🖼️ **Image Generation** | AI image creation via Hugging Face (Stable Diffusion XL) |
| 📝 **Content Writer** | Generate essays, letters, songs, stories, and more |
| 🧠 **Decision Model** | Intent classification using Cohere Command XL |
| 🖥️ **App Automation** | Open/close apps, control system volume, search YouTube & Google |
| 🎨 **Modern GUI** | Frameless PyQt5 interface with animated GIF and chat screen |

---

## 🗂️ Project Structure

```
Spider-AI/
│
├── Backend/
│   ├── Automation.py          # App/system/content automation logic
│   ├── Chatbot.py             # Groq-powered conversational AI
│   ├── ImageGeneration.py     # Hugging Face image generation
│   ├── Model.py               # Cohere intent/decision classification
│   ├── RealtimeSearchEngine.py# Google search + Groq response engine
│   ├── SpeechToText.py        # Selenium-based voice recognition
│   ├── TextToSpeech.py        # Edge TTS + Pygame audio playback
│   └── Data/
│       └── ChatLog.json       # Persistent chat history
│
├── Data/                      # Runtime data & AI-generated content
│   ├── ChatLog.json
│   ├── Voice.html
│   └── *.txt / *.jpg          # Generated content and images
│
├── Frontend/
│   ├── GUI.py                 # PyQt5 graphical user interface
│   ├── Files/
│   │   ├── Database.data
│   │   ├── ImageGeneration.data
│   │   ├── Mic.data           # Microphone state flag
│   │   ├── Responses.data     # Latest assistant response
│   │   └── Status.data        # Assistant status text
│   └── Graphics/
│       ├── spider.gif         # Animated assistant visual
│       ├── Mic_on.png
│       ├── Mic_off.png
│       ├── Home.png
│       ├── Chats.png
│       ├── Maximize.png
│       ├── Minimize.png
│       ├── Minimize2.png
│       ├── Close.png
│       └── Settings.png
│
├── main.py                    # Main entry point (orchestrator)
├── Requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
└── .gitignore
```

---

## 🧠 Architecture Overview

```
User Voice Input
      │
      ▼
SpeechToText.py  ──────────────────────────────────────────┐
      │                                                    │
      ▼                                                  GUI.py
Model.py (Cohere)                                     (PyQt5 Frontend)
  Intent Classification                                     │
      │                                                     │
  ┌───┴──────────────────────────────────────────────┐      │
  │                                                  │      │
  ▼                ▼              ▼          ▼        ▼     │
Chatbot.py   RealtimeSearch   Automation  ImageGen  Content │
(Groq LLaMA) (Google+Groq)   (Apps/Sys) (HuggingFace)      │
  │               │              │         │       │    │
  └───────────────┴───────────────┴──────────┴────────┘     │
                          │                                 │
                          ▼                                 │
                  TextToSpeech.py ──────────────────────────| 
                  (Edge TTS + Pygame)
```

---

## ⚙️ Backend Modules

### 🤖 `Chatbot.py`
- Uses **Groq API** with `llama-3.1-8b-instant`
- Maintains full conversation history in `Data/ChatLog.json`
- Injects real-time date/time context into every request
- Streams responses for low latency

### 🌐 `RealtimeSearchEngine.py`
- Performs live **Google Search** using the `googlesearch-python` library
- Passes top 5 results to **Groq LLaMA** for a synthesized answer
- Ideal for queries needing up-to-date, factual responses

### 🧠 `Model.py`
- Uses **Cohere Command XL** to classify user intent
- Converts natural language into structured task commands like:
  - `open chrome`, `play <song>`, `google search <topic>`, `generate image <prompt>`
- Supports multi-intent parsing in a single query

### 🛠️ `Automation.py`
- Executes classified commands asynchronously
- Supports: open/close apps, YouTube play, Google search, content writing, system commands
- Content writing uses **Groq LLaMA 3.3 70B** and saves output to `.txt` files

### 🖼️ `ImageGeneration.py`
- Calls **Hugging Face** Stable Diffusion XL API
- Generates 4 high-quality images per prompt concurrently using `asyncio`
- Saves images to `Data/` and opens them automatically

### 🎤 `SpeechToText.py`
- Launches a local HTML page in **Chrome** via Selenium
- Uses browser's native **Web Speech API** for real-time transcription
- Supports multilingual input with auto-translation to English via `mtranslate`

### 🔊 `TextToSpeech.py`
- Generates speech using **Microsoft Edge TTS** (`edge-tts`)
- Plays audio via **Pygame mixer**
- For long responses (>250 chars), speaks only the first 2 sentences and displays the rest in chat

---

## 🎨 Frontend — `GUI.py`

Built with **PyQt5**, the interface features:

- **Frameless window** with custom draggable top bar
- **Home Screen** — fullscreen animated `spider.gif` with mic toggle button
- **Chat Screen** — scrollable dark-themed chat with white text
- **Status Label** — real-time assistant status (e.g., "Listening...", "Thinking...")
- **Navigation** — Home and Chat buttons in the top bar
- **Mic Toggle** — click to start/stop voice input (updates `Mic.data`)
- **File-based IPC** — GUI polls `Responses.data` and `Status.data` every 100ms for updates from the backend

---

## 🔧 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/vikashkr96/Spider-AI.git
cd Spider-AI
```

### 2. Install Dependencies
```bash
pip install -r Requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```env
Username=YourName
Assistantname=Spider
GroqAPIKey=your_groq_api_key
CohereAPIKey=your_cohere_api_key
HuggingFaceAPIKey=your_huggingface_api_key
AssistantVoice=en-CA-LiamNeural
InputLanguage=en-US
```

### 4. Run the Assistant
```bash
python main.py
```

---

## 📦 Requirements

```
groq
cohere
pyqt5
edge-tts
pygame
selenium
webdriver-manager
mtranslate
requests
beautifulsoup4
pywhatkit
AppOpener
rich
python-dotenv
Pillow
keyboard
```

> Install all at once: `pip install -r Requirements.txt`

---

## 🌐 API Keys Required

| Service | Purpose | Get it at |
|---|---|---|
| **Groq** | Chatbot + Content Writing | [console.groq.com](https://console.groq.com) |
| **Cohere** | Intent Classification | [dashboard.cohere.com](https://dashboard.cohere.com) |
| **Hugging Face** | Image Generation | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |

---

## 💬 Example Commands

| You Say | What Happens |
|---|---|
| `"Open Chrome"` | Launches Chrome |
| `"Play Bairan song"` | Plays the song on YouTube |
| `"What is the weather today?"` | Real-time web search answer |
| `"Generate image of a futuristic city"` | Creates 4 AI images |
| `"Write an essay on climate change"` | Generates & opens in Notepad |
| `"Google search Python tutorials"` | Opens Google search |
| `"Volume up"` | Increases system volume |
| `"Close Spotify"` | Closes the app |

---

## 🔮 Planned Features (Roadmap)

- [ ] Complete `main.py` orchestrator to wire all modules together
- [ ] Reminder scheduling system
- [ ] Memory/personality persistence across sessions
- [ ] Wake word detection ("Hey Spider")
- [ ] Plugin system for custom commands
- [ ] Mobile companion app

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Vikash Kumar**
- GitHub: [@vikashkr96](https://github.com/vikashkr96)

---

<p align="center">
  Made with ❤️ and Python · Spider AI — Your Personal Desktop Assistant
</p>