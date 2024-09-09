import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import settings


def send_invite_code_to_email(email: str, code: int) -> None:
    """Отправляет проверочный код на указанную электронную почту.

    :param email: Адрес электронной почты, на который будет отправлен код.
    :param code: Проверочный код, который будет отправлен.
    """
    sender_email = settings.SENDER_EMAIL  # Замените на ваш адрес электронной почты
    sender_password = settings.SENDER_PASSWORD  # Замените на ваш пароль

    # Создаем сообщение
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = "Ваш проверочный код"

    # Тело сообщения
    body = f"Ваш проверочный код: {code}. Пожалуйста, используйте код для подтверждения вашей учетной записи."
    msg.attach(MIMEText(body, "plain"))

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Защита соединения
            server.login(sender_email, sender_password)  # Вход в учетную запись
            server.sendmail(sender_email, email, msg.as_string())  # Отправка письма

        print(f"Письмо c кодом успешно отправлено на {email}.")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
