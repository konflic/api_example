# api_example

This is an API example for testing and demo purposes.

## Setup

Before starting the application environment variables should be set to define admin user

```
export LOGIN=admin
export PASSWORD=admin
```
You can setup with venv

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -Ur requirements.txt
```

Or use docker instead

```bash
docker build -t api_example .
ADMIN=admin PASSWORD=admin docker run -p 5000:5000 api_example -d
```
