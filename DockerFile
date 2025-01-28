# Step 1: Use official Python base image
FROM python:3.13.1-slim

# Step 2: Set the working directory to /app
WORKDIR /app

# Step 3: Copy everything into the container's working directory
COPY . /app

# Step 4: Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 5: Expose the port Flask will run on
EXPOSE 5000

# Step 6: Set environment variables for Flask app
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Step 7: Command to run the Flask app
CMD ["python", "main.py"]