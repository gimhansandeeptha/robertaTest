# Choose our version of Python
FROM python:3.12

# Set up a working directory
WORKDIR /app

# Copy just the requirements into the working directory so it gets cached by itself
COPY ./requirements.txt /app/requirements.txt

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the code into the working directory
COPY ./src /code/app

# Tell uvicorn to start spin up our code, which will be running inside the container now
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
