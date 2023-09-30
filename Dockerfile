# Use Python 3.11.5 as the base image
FROM python:3.11.5

# Set the working directory to /DisBotPython
WORKDIR /DisBotPython

COPY . /DisBotPython/

# Install the required packages
RUN pip install -r requirements.txt

# Expose port 10000
ENV PORT=10000
EXPOSE ${PORT}

# Run main.py when the container launches
CMD python main.py