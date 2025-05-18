from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import cv2
import numpy as np

app = FastAPI()

video_path = "mustard.mp4"
cap = cv2.VideoCapture(video_path)

TARGET_PIXELS = 125 * 65  # ~37,500 pixels total

@app.get("/grid")
def get_grid():
    global cap

    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    aspect_ratio = original_width / original_height
    new_height = int((TARGET_PIXELS / aspect_ratio) ** 0.5)
    new_width = int(aspect_ratio * new_height)

    resized = cv2.resize(frame, (new_width, new_height))
    rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    hex_colors = []
    for row in rgb_frame:
        for r, g, b in row:
            hex_colors.append('#{:02x}{:02x}{:02x}'.format(r, g, b))

    return {
        "width": new_width,
        "height": new_height,
        "colors": hex_colors
    }

@app.post("/send")
async def receive_data(request: Request):
    data = await request.json()
    print("Received:", data)
    return {"status": "ok", "echo": data}
