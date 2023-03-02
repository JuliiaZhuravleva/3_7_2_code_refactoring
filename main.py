from gmail import Gmail
import configparser


def get_auth_data():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    login = config['login_info']['login']
    password = config['login_info']['password']
    return {'login': login, 'password': password}


def get_mail_to_send():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    recipients = config['mail']['recipients'].split(',')
    subject = config['mail']['subject']
    message = config['mail']['message']
    return {'recipients': recipients, 'subject': subject, 'message': message}


if __name__ == '__main__':
    my_gmail = Gmail(**get_auth_data())
    my_gmail.send_message(**get_mail_to_send())
    my_last_message = my_gmail.receive_message()
    print(my_last_message)
