import os
import datetime

def validate_path(path, path_type="file"):
    """
    Validate the existence of a file or directory.
    :param path: Path to validate.
    :param path_type: "file" or "directory".
    :return: Boolean indicating whether the path exists.
    """
    if path_type == "file":
        return os.path.isfile(path)
    elif path_type == "directory":
        return os.path.isdir(path)
    else:
        raise ValueError("Invalid path_type. Use 'file' or 'directory'.")

def create_save_dir(base_dir="/app/runs/predict"):
    """
    Generate a unique directory for saving predictions based on the current timestamp.
    :param base_dir: Base directory for saving results.
    :return: Path to the created directory.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = os.path.join(base_dir, timestamp)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir

def log_message(message, log_file="/app/logs/detection.log"):
    """
    Log a message to a specified log file.
    :param message: Message to log.
    :param log_file: Path to the log file.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

