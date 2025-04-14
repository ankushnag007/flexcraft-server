import os
from email.message import EmailMessage
from string import Template

from aiosmtplib import SMTP

from . import SMTP_EMAIL, SMTP_PASS, SMTP_PORT, SMTP_SERVER


async def send_mail_html(
    message: str,
    subject: str,
    receiver_email: str,
    cc_email: str = [],
):
    try:
        smtp_server = SMTP_SERVER
        port = SMTP_PORT
        sender_email = SMTP_EMAIL
        password = SMTP_PASS
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = sender_email
        email["To"] = receiver_email
        if len(cc_email) != 0:
            email["cc"] = [mails.split(",") for mails in cc_email if mails][0]
        email.set_content(message, subtype="html")
        # Send the message via local SMTP server.
        client = SMTP(hostname=smtp_server, port=port, timeout=10, start_tls=True)
        await client.connect()
        # await client.starttls()
        # s.ehlo()  # Can be omitted, just added to ping smtp server before login
        await client.login(sender_email, password)
        await client.send_message(email)
    except Exception as e:
        print(e)
        return {"message": str(e), "status": 400}


def substitute_variables(template: str, data_dict: dict) -> str:
    """
    The function `substitute_variables` takes a template string and a dictionary of data, and replaces
    variables in the template with corresponding values from the data dictionary.

    :param template: The `template` parameter is a string that contains placeholders for variables that
    need to be substituted with values from the `data_dict`. For example, the template could be "Hello,
    $name!" where `$name` is a placeholder for the actual name value that will be substituted from the
    `data
    :type template: str
    :param data_dict: The `substitute_variables` function takes in two parameters:
    :type data_dict: dict
    """

    try:
        string_sub = Template(template)
        string_sub = string_sub.safe_substitute(data_dict)
        return string_sub
    except Exception as e:
        return {"message": str(e), "status": 400}
