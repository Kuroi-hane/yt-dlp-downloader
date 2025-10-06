from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/api/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url="}), 400

    try:
        # run yt-dlp to get direct video URL
        result = subprocess.run(
            [
    "yt-dlp",
    "--cookies", "/etc/secrets/cookies.txt",
    "--no-cache-dir",
    "-f", "b[ext=mp4]/bv*+ba/b",
    "-j",
    url
],
            capture_output=True, text=True, check=True
        )
        video_url = result.stdout.strip()
        return jsonify({"video_url": video_url})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "yt-dlp downloader API is live 🎥", 200
