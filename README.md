Here’s a draft for your `README.md` file to document your project:

---

# Markdown to ElevenLabs

**Markdown to ElevenLabs** is an open-source project that converts Markdown files into high-quality voiceovers using the [ElevenLabs Text-to-Speech API](https://www.elevenlabs.io). The project is designed for creating natural-sounding audio from written content, ideal for podcasts, audiobooks, and more.

---

## Features
- **Markdown Parsing**: Splits Markdown files into sections, intelligently grouping paragraphs and lists.
- **Text-to-Speech Conversion**: Uses ElevenLabs API to generate realistic voiceovers with customizable voice settings.
- **Audio Processing**: Combines generated audio sections into a single cohesive file, complete with natural pauses.
- **Flexible Operation Modes**:
  - Process Markdown only (`--markdown-only`).
  - Generate audio only (`--audio-only`).
  - Combine existing audio files only (`--combine-only`).
- **Error Handling and Preprocessing**:
  - Cleans and normalizes text for smooth audio generation.
  - Handles special characters (`—`, `…`, etc.) gracefully.

---

## Installation

### Prerequisites
- Python 3.8 or newer
- ElevenLabs API Key ([Get yours here](https://www.elevenlabs.io))
- Dependencies:
  - Install `pydub` for audio manipulation.
  - Install `dotenv` for environment variable management.
  - Install `unidecode` for text normalization.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Requirements File
Ensure the following dependencies are listed in your `requirements.txt`:
```txt
elevenlabs
pydub
python-dotenv
unidecode
```

### Copy Environment Variables File

The CLI command to copy `.env.example` to `.env` is:

### Linux or macOS
```bash
cp .env.example .env
```

### Windows (Command Prompt)
```cmd
copy .env.example .env
```

### Windows (PowerShell)
```powershell
Copy-Item .env.example .env
```

### Add Environment Variables

1. Log in to your [ElevenLabs account](https://elevenlabs.io/app/sign-in) and [generate an API key](https://elevenlabs.io/app/settings/api-keys).
2. Copy your API key and voice ID to the `.env` file:
   ```env
   ELEVENLABS_API_KEY=your_api_key_here
   ELEVENLABS_VOICE_ID=your_voice_id_here
   ```

---

## Usage

Here’s the updated section of the `README.md` file:

---

### 1. Prepare Markdown Files
Place your Markdown files in the `markdown` folder located in the project root. Before running the script, review and edit these files as needed:
- Remove any content you don't want included, such as:
  - Code blocks
  - Tables of contents
  - Superfluous headings or sections
- Ensure the text is structured logically for audio generation.

After editing, the script will process the Markdown files and split them into individual sections for audio conversion.

### 2. Run the Script
```bash
python main.py [options]
```

### Options
| Option          | Description                                                                                     |
|------------------|-------------------------------------------------------------------------------------------------|
| `--reset`        | Deletes previous output files and starts fresh.                                                |
| `--audio-only`   | Skips Markdown processing and generates audio for existing Markdown sections.                  |
| `--markdown-only`| Processes Markdown files only, without generating audio.                                       |
| `--combine-only` | Combines existing audio files into a single cohesive file.                                     |
| `--voice-id`     | Specify a voice ID (overrides `.env`).                                                         |
| `--api-key`      | Specify an API key (overrides `.env`).                                                         |

### Example Commands
#### Full Pipeline (Markdown → Audio → Combined File)
```bash
python main.py --reset
```

#### Markdown Parsing Only
```bash
python main.py --markdown-only
```

#### Audio Generation Only
```bash
python main.py --audio-only
```

#### Combine Existing Audio Files
```bash
python main.py --combine-only
```

---

## File Structure
```
markdown-to-elevenlabs/
├── main.py                   # Main entry point for the program
├── src/
│   ├── split_markdown.py     # Splits Markdown files into sections
│   ├── build_output.py       # Handles audio generation and combination
├── markdown/                 # Input Markdown files
├── output/
│   ├── markdown/             # Processed Markdown sections
│   ├── audio/                # Generated audio files
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
```

---

## Contributing
Contributions are welcome! To get started:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed explanation.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments
- **ElevenLabs** for their industry-leading Text-to-Speech API.
- **pydub** for seamless audio processing.
- **open-source contributors** for making projects like this possible!