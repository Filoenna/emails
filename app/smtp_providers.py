import os

from dotenv import load_dotenv
from . import provider

load_dotenv()


class SMTPProvider(provider.Provider):
    def __init__(self, name):
        self.username = os.getenv(name + "_MAIL_PASSWORD")
        self.password = os.getenv("GOOGLE_MAIL_PASSWORD")
        self.port = int(os.getenv(name + "_MAIL_PORT"))
        self.server = os.getenv(name + "_MAIL_SERVER")
        self.tls = os.getenv(name + "_MAIL_TLS")
        self.ssl = os.getenv(name + "_MAIL_SSL")
        self.credentials = os.getenv(name + "_USE_CREDENTIALS")
        self.validate_certs = os.getenv(name + "_VALIDATE_CERTS")
