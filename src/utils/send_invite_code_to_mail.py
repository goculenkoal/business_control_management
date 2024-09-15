import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import settings


def send_invite_code_to_email(recipient_email: str, code: int) -> None:
    """Отправляет проверочный код на указанную электронную почту.

    :param recipient_email: Адрес электронной почты, на который будет отправлен код.
    :param code: Проверочный код, который будет отправлен.
    """
    sender_email = settings.SENDER_EMAIL  # Замените на ваш адрес электронной почты
    sender_password = settings.SENDER_PASSWORD  # Замените на ваш пароль

    subject = "Ваш проверочный код"
    body = f"Ваш проверочный код: {code}. Пожалуйста, используйте код для подтверждения вашей учетной записи."

    # Создаем сообщение
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Тело сообщения

    msg.attach(MIMEText(body, "plain"))

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Защита соединения
            server.login(sender_email, sender_password)  # Вход в учетную запись
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Отправка письма

        print(f"Письмо c кодом успешно отправлено на {recipient_email}.")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


def send_invite_token_link_email(recipient_email: str, code: str | int) -> None:
    """Отправляет проверочный код на указанную электронную почту.

    :param recipient_email: Адрес электронной почты, на который будет отправлен код.
    :param code: Проверочный код, который будет отправлен.
    """
    sender_email = settings.SENDER_EMAIL  # Замените на ваш адрес электронной почты
    sender_password = settings.SENDER_PASSWORD  # Замените на ваш пароль

    confirm_link = f"http://yourdomain.com/confirm_registration/{code}"
    subject = "Подтверждение регистрации"
    body = f"Пожалуйста, перейдите по следующей ссылке для подтверждения регистрации: {confirm_link!r}"

    # Создаем сообщение
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Тело сообщения

    msg.attach(MIMEText(body, "plain"))

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Защита соединения
            server.login(sender_email, sender_password)  # Вход в учетную запись
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Отправка письма

        print(f"Письмо c кодом успешно отправлено на {recipient_email}.")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
