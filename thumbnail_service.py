from flask import Flask, request, send_file, jsonify
import cv2
import os
import uuid

app = Flask(__name__)
os.makedirs("thumbnails", exist_ok=True)

@app.route("/thumbnail", methods=["POST"])
def generate_thumbnail():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No video uploaded"}), 400

    uid = uuid.uuid4().hex
    input_path = f"video_{uid}.mp4"
    thumbnail_path = f"thumbnails/thumbnail_{uid}.jpg"
    file.save(input_path)

    cap = cv2.VideoCapture(input_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(thumbnail_path, frame)
        cap.release()
        os.remove(input_path)
        return send_file(thumbnail_path, mimetype="image/jpeg")
    else:
        cap.release()
        return jsonify({"error": "Could not extract frame"}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Thumbnail service running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
