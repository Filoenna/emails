from email.message import EmailMessage
import os.path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from . import mail
from . import provider


class GoogleApiProvider(provider.Provider):

    CLIENT_FILE: str
    API_NAME: str = "gmail"
    API_VERSION: str = "v1"
    SCOPES: list = ["https://www.googleapis.com/auth/gmail.send"]
    TOKEN: str = "token.json"

    def credentials(self):
        creds = None
        if os.path.exists(self.TOKEN):
            creds = Credentials.from_authorized_user_file(self.TOKEN, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./app/credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open(self.TOKEN, "w") as token:
                token.write(creds.to_json())
        return creds

    def create_service(self):

        creds = self.credentials()

        try:
            # Call the Gmail API
            service = build(self.API_NAME, self.API_VERSION, credentials=creds)
            return service

        except HttpError as error:
            print(f"An error occurred: {error}")

    def prepare_message(self, email: mail.EmailSchema):
        # message = MIMEText("This is automated mail.", 'html') <- do wysyłania szablonów
        # message = mail.Mail()
        message = EmailMessage()
        message.set_content(email.body)
        message["To"] = email.email
        message["From"] = "machefi1@gmail.com"
        message["Subject"] = email.subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return encoded_message

    def send_mail(self, encoded_message):
        try:
            create_message = {"raw": encoded_message}

            service = self.create_service()
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message ID: {send_message["id"]}')

        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message
