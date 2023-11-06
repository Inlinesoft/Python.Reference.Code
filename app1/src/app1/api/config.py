import os


def parse_creds():
    uids = os.environ.get("API_USERNAME", "").split(",")
    pwds = os.environ.get("API_PASSWORD", "").split(",")
    return dict(zip(uids, pwds))


class Config:
    API_STAGE = os.environ.get("API_STAGE", "")
    API_CREDENTIALS = parse_creds()
    API_HOST = os.environ.get("API_HOST", "")
    API_PORT = int(os.environ.get("API_PORT", "8000"))
    API_CORS_ORIGINS = os.environ.get("API_CORS_ORIGINS", "").split(",")
