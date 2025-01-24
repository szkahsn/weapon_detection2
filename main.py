from ultralytics import YOLO
import cv2
import sys
import datetime
from utils import validate_path, log_message

# Load the trained YOLOv8 model
try:
    model = YOLO('/app/weights/best.pt')
except Exception as e:
    log_message(f"Error loading model: {e}")
    sys.exit("Error loading YOLO model.")

# Choose input source
def get_input_source():
    print("Choose input source:")
    print("1. Live camera (default)")
    print("2. Video file")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "2":
        video_path = input("Enter the path to your video file: ").strip()
        if not validate_path(video_path, "file"):
            log_message(f"Error: Video file not found at {video_path}.")
            sys.exit("Error: Video file not found.")
        return video_path
    else:
        print("Using live camera as input.")
        return 0

# Process live camera input
def process_live_camera(model):
    print("Starting live detection. Press 'q' to quit.")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        log_message("Error: Unable to access the camera.")
        sys.exit("Error: Unable to access the camera.")

    # Initialize video writer
    video_save_path = f"/app/runs/live_video/output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 video
    out = cv2.VideoWriter(video_save_path, fourcc, 20.0, (640, 480))  # 20 FPS, resolution 640x480

    while True:
        ret, frame = cap.read()
        if not ret:
            log_message("Error: Unable to read frame from the camera.")
            break

        try:
            # Resize frame and run YOLOv8 inference
            frame = cv2.resize(frame, (640, 480))
            results = model.predict(frame, conf=0.2)
            annotated_frame = results[0].plot()

            # Display annotated frame in popup window
            # cv2.imshow("YOLOv8 Live Detection", annotated_frame)

            # Write annotated frame to video file
            out.write(annotated_frame)

        except Exception as e:
            log_message(f"Error during live detection: {e}")
            break

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    log_message(f"Video saved to {video_save_path}.")
    print("Live detection ended.")

# Main Execution
input_source = get_input_source()
if input_source == 0:
    process_live_camera(model)
else:
    try:
        video_save_path = f"/app/runs/video_output/output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        results = model.predict(source=input_source, conf=0.2, save=True, save_dir=video_save_path)

        # Display results frame-by-frame in a popup window
        for frame in results:
            cv2.imshow("YOLOv8 Video Detection", frame.plot())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        log_message(f"Inference complete. Results saved to {video_save_path}.")
    except Exception as e:
        log_message(f"Error during inference: {e}")
