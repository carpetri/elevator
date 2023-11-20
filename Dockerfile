FROM python:3.12-slim
WORKDIR /elevator
COPY . /elevator
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "elevatorSystemSimulator.py"]
