# Video-downloader
A personal project built for me to learn about stream handling, thread pooling, video conversion, and working with external APIs. For educational use only.
- It is a multithreaded way to download videos from youtube.
- It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to get the streaming URLs (mainly cause of the proof of origin tokens).
- The output WILL be separated into two files (audio and video/frames).

# Disclaimer

This project is intended for **educational and personal use only**. It was created as a learning exercise to explore concepts such as stream handling, format conversion, and API interaction.

This tool is **not intended** to be used to download, convert, or reproduce any copyrighted material without the explicit permission of the copyright holder. Downloading or converting copyrighted content without authorization may violate applicable copyright laws and the Terms of Service of the platform in question.

The developer assumes **no liability** for any misuse of this software or for any legal consequences arising from its use in violation of copyright law or platform terms of service.

**Users are responsible** for ensuring that their use of this tool complies with all applicable laws and regulations in their jurisdiction, as well as the Terms of Service of any platforms they interact with.

## Getting Started
### Prerequisites

- Python 3.13+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sab-992/video-downloader.git
cd video-downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Change the VIDEO_URL, RESOLUTION and FPS constants in the **"main.py"** file and run with:
```bash
python main.py
```

### View Logs
If any error happened during, they can be logged by enabling the setting in the utils/settings.py file. The logs will be saved in detail the utils/logs/details folder or simply in the utils/logs/logs.txt file.
