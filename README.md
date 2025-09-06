# Lightweight PNGTuber

A minimal **PNGTuber** application written in Python with Tkinter.  
This app displays a simple 2D model that blinks, reacts to microphone input for mouth movement, and responds to keyboard input for accessories, faces, and arm animation.

The program is started using **Run_Vtuber.vbs**.

---

## Features

- **Blinking animation** (automatic eye blinking).
- **Mouth movement** that reacts to microphone audio input.
- **Keyboard control**:
  - **F1** → cycle through accessories.
  - **F2** → cycle through face states.
  - Any other key → triggers arm up animation.
- **Accessory & face overlays** with support for a `!nothing.png` placeholder (transparent).
- **Lightweight & simple**: only requires Python and a few libraries.

---

## Requirements

- Python 3.8+
- The following Python packages:
  ```bash
  pip install pillow sounddevice numpy keyboard
  ```

---

## File Structure

```
project-root/
│
├── Run_Vtuber.vbs         # Script to launch the app
├── main.py                # PNGTuber Python script (this repo's code)
├── model/
│   ├── base.png           # Base model image
│   ├── mouth_open.png     # Mouth open image
│   ├── eyes_closed.png    # Eyes closed image
│   ├── arm_up.png         # Arm raised image
│   ├── !nothing.png       # Transparent placeholder
│   ├── accessories/       # Accessory images
│   │   └── !nothing.png
│   └── face_states/       # Face overlay images
│       └── !nothing.png
```

---

## Usage

1. Place your model assets inside the `model/` folder:
   - `base.png` → your default character image.
   - `mouth_open.png` → mouth animation frame.
   - `eyes_closed.png` → closed eyes for blinking.
   - `arm_up.png` / `!nothing.png` → arm animation frames.
   - `model/accessories/` → accessory images (e.g., hats, props).
   - `model/face_states/` → face overlay images (e.g., expressions).
2. Run the program with the included VBScript:
   ```
   double-click Run_Vtuber.vbs
   ```
   or run it manually with:
   ```bash
   python main.py
   ```
3. The **Model Window** will appear. Speak into your microphone to see the mouth move.

---

## Controls

- **F1** → Cycle through accessories.
- **F2** → Cycle through face overlays.
- **Any key press** → Arm raises briefly.
- **Release key** → Arm lowers.

---

## Error Logging

If an error occurs, details will be saved to:
```
error_log.txt
```

---

## Notes

- `!nothing.png` is used as a **transparent placeholder** for hiding layers (accessories, faces, arm down state, etc.).
- You can replace the placeholder with your own transparent PNGs of any size.
- Background color is set to `#12ff06` (green) by default, so you can chroma-key it for streaming.

---

## License

MIT License — feel free to use, modify, and distribute.
