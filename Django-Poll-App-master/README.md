# Fingerprint Website Login - Webauthn

## Setup

Set .env
```
cp .env.example .env
```

Then

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
## Run locally
```
uvicorn --reload main:app
```

Visit: http://localhost:8000/

# Reading

- https://www.w3.org/TR/webauthn-2/
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API#registration
