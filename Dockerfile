# Step 1: Use Python 3.10 slim base image
FROM python:3.10-slim

# Step 2: Set environment variables to minimize Python buffer issues
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the requirements file to the working directory
COPY requirements.txt /app/

# Step 5: Install system-level dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the project files to the container
COPY . /app/

# Step 8: Create necessary directories for outputs
RUN mkdir -p /app/runs/live_frames /app/runs/predict /app/logs /app/weights

# Step 9: Ensure the weights file is present in the right directory
COPY weights/best.pt /app/weights/

# Step 10: Expose any required port (optional)
EXPOSE 8080

# Step 11: Define the default command to run the application
CMD ["python", "main.py"]
