import os
from email.message import EmailMessage
from string import Template

from aiosmtplib import SMTP

from . import SMTP_EMAIL, SMTP_PASS, SMTP_PORT, SMTP_SERVER


async def send_mail_html(
    message: str,
    subject: str,
    receiver_email: str,
    cc_email: list[str] = None,
):
    try:
        smtp_server = "smtp.office365.com"
        port = 587
        sender_email = "msmohitsharma144@outlook.com"
        password = SMTP_PASS  # Use an **App Password** if MFA is enabled

        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = sender_email
        email["To"] = receiver_email
        if cc_email:
            email["Cc"] = ", ".join(cc_email)
        email.set_content(message, subtype="html")

        client = SMTP(hostname=smtp_server, port=port, timeout=10, start_tls=True)
        await client.connect()
        await client.login(sender_email, password)
        await client.send_message(email)
        await client.quit()

        return {"message": "Email sent successfully", "status": 200}

    except Exception as e:
        print("EMAIL ERROR:", str(e))
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
