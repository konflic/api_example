# api_example

This is an API example for testing and demo purposes.

## Description

App allows to store data for users and assign them with grades.

## Setup

Prior to starting the application environment variables should be set to define admin user of the application.

```
export LOGIN={admin password}
export PASSWORD={admin password}
```

You can setup project with venv

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -Ur requirements.txt
```

Run service
```
python app.py
```

Or use docker instead

```bash
docker build -t api_example .
docker run -p 8888:8888 -e PORT=8888 -e LOGIN={admin login} -e PASSWORD={admin password} api_example
```
