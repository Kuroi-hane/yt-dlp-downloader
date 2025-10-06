from flask import Flask, request, jsonify
import subprocess, json, shutil, os

app = Flask(__name__)

@app.route("/")
def home():
    return "API live"

@app.route("/api/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url="}), 400

    # Copy cookie file to /tmp
    COOKIE_SRC = "/etc/secrets/cookies.txt"
    COOKIE_TMP = "/tmp/cookies.txt"
    if os.path.exists(COOKIE_SRC):
        shutil.copy(COOKIE_SRC, COOKIE_TMP)

    cmd = [
        "yt-dlp",
        "--cookies", COOKIE_TMP,
        "--no-cache-dir",
        "-f", "b[ext=mp4]/bv*+ba/b",
        "-j",
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        data = json.loads(result.stdout)
        return jsonify({
            "title": data.get("title"),
            "duration": data.get("duration"),
            "thumbnail": data.get("thumbnail"),
            "video_url": data.get("url"),
        })
    except Exception as e:
        return jsonify({"error": str(e)})
