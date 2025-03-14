# Use an official Python image as a base
FROM python:3.10

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY app/ .

# Expose necessary ports (8501 for Streamlit, 8000 if an API is needed)
EXPOSE 8501 

# Ensure environment variables are set (optional)
ENV PYTHONUNBUFFERED=1

# Start Streamlit UI when the container runs
CMD ["streamlit", "run", "ui.py"]