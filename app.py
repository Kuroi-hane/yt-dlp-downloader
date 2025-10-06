import os, shutil, subprocess, json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing ?url="}), 400

    COOKIE_SRC = "/etc/secrets/cookies.txt"
    COOKIE_TMP = "/tmp/cookies.txt"

    # copy to writable dir
    try:
        shutil.copy(COOKIE_SRC, COOKIE_TMP)
    except Exception:
        pass

    cmd = [
        "yt-dlp",
        "--cookies", COOKIE_TMP,
        "--no-cache-dir",
        "--no-overwrites",          # prevents writes
        "-f", "b[ext=mp4]/bv*+ba/b",
        "-j", url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
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
