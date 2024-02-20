FROM python:3.12-bookworm

WORKDIR ./app

COPY requirements.txt requirements.txt
 
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "notebook",  "--ip='*'", "--port=8888",  "--no-browser", "--allow-root"] 