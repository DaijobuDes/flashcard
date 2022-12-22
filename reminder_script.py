import sqlite3
import datetime
import time
import smtplib, ssl

# Reference: https://realpython.com/python-send-email/#sending-a-plain-text-email

SMTP_PORT = 465
SMTP_EMAIL = "cs342flashcard@gmail.com"
SMTP_PASSWORD = "hdoidmdccqzfjukk"

context = ssl.create_default_context()

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

def sendEmail():
    with smtplib.SMTP_SSL("smtp.gmail.com", SMTP_PORT, context=context) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        while True:
            todays_date = datetime.datetime.now()
            minutes_after = datetime.datetime.now() + datetime.timedelta(minutes=5)

            reminders = cursor.execute(f"SELECT * FROM lexicard_web_reminders WHERE reminder_timestamp >= '{todays_date}' AND reminder_timestamp <= '{minutes_after}'")

            for i in reminders.fetchall():

                user_data_temp = cursor.execute(f"SELECT * FROM lexicard_web_user WHERE user_id = {i[5]}")
                user_data = user_data_temp.fetchone()

                subject = f'Subject: Lexicard Reminder - {i[1]}'
                message = f'Hi {user_data[2]}, your reminder ({i[2]}) has a timestamp of {i[4]} has initiated an automated email notification.'

                text_plain = subject + "\n\n" + message

                server.sendmail(SMTP_EMAIL, user_data[3], text_plain)
                cursor.execute(f"DELETE FROM lexicard_web_reminders WHERE reminder_id = {i[0]}")
                cursor.execute(f"INSERT INTO lexicard_web_messages (timestamp, message_body, user_id_id) VALUES ('{datetime.datetime.now()}', '{message}', {i[5]})")
                connection.commit()

                print("Record deleted.")

            if reminders.rowcount <= 0:
                print("No emails.")
            else:
                print("Sent emails")
            time.sleep(180)

def main():
    sendEmail()

if __name__ == '__main__':
    main()