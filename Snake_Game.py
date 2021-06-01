import pygame
import random
import clipboard
import socket
import pickle
import json
import sys
from urllib.request import urlopen
import uuid
import re
from validate_email import validate_email
import threading
import smtplib  # For Send main it's very importent
from email.mime.text import MIMEText  # to add additional perametar in mail
from email.mime.multipart import MIMEMultipart  # to add additional perametar in mail
from email.mime.base import MIMEBase
from email import encoders  # To encode file into msg formate.
import gspread #For google sheet
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt

pygame.init()

def load_sound(sound_file):
    return pygame.mixer.Sound(sound_file)

def play_sound(sound_file,loop = 0,maxmim_time = None):
    if maxmim_time == None:
        pygame.mixer.Sound.play(sound_file, loop)
    else:
        pygame.mixer.Sound.play(sound_file, loop, maxmim_time)

def set_valuem(sound_file, valuem):
    #Max Value 1.0
    #Min Value 0.0
    pygame.mixer.Sound.set_volume(sound_file, valuem)


Online_status = False
Playing_Status = False
Local_high_score = 0
Online_High_score = 0
Online_High_score_name = ''
Online_High_score_email = ''

class google_sheet:
    global Online_status
    def __init__(self,sheet_name, secret_json_file = ""):
        self.sheet_opend = False
        self.sheet_name = sheet_name
        self.secret_file = secret_json_file
    def open_sheet(self):
        try:
            scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                     "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
            creds_type = "service_account"
            service_account_email = "feedback@snake-game-235916.iam.gserviceaccount.com"
            private_key_pkcs8_pem = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZBgHcvjuO+kl3\n/vlf+86FoZBmcWGkKygLnTCMepEebQjlLN+ZzecV9QPGTaJdUvCAPa6hcmBJhXsq\nOBxwmGxD084KXwMeDrH0FTl0MNgukjfuS0ztqUb2oTwMPC5v2zC3eXx7FbUy/JDr\n/wdDcE7GnLgfpbZGT14v/mctdtP6OyoG69z8/2ohla7UzZ8AQ35snOnFxV9oSzln\nMH1lu/6mfR8bs+sjeAIVa+fDjbzucBjnGaTHdBZUfxzacbk2yqDdH+50swhVMohP\nRIWFOghlB5ebC1pKxk51Fdu5SRuY5dp0YKSBpFfFopQNDC36JFI2KuVyJNrEkzmw\nKh+oBOk7AgMBAAECggEAHKX0xExzHw35ojcAnfkpDXiVbbBtbMxNl3sKw0oRECau\noyU3CXb0e/ZeigovyxQDhabGomAk6a7NQ7a0kFng7wPgz61BCqgKpd0xX/DjEDj8\nsqazVM07xWGjOdEsinF5WegrJ2oFffGt+hjJVdVZUjK1/+rIyLoEMq0IyQi1n+OY\nmlOatgHZYm5qTJW3GDC2LB/b6PrquwTWvLrdgZbBZw2EvkVscte1H4s1pmKGKY9A\nSq+b34F7i6UBSpCOAzghabF17ovOmOwT2Ijhv76oggjnV7zyJf2Zv9jiezdMqCUw\nODEfkd9hIcvbNiyG4v8jeMBHY66FGqZl6DNZP757nQKBgQDHpuWMUfZbk1eu1XEz\nqvCKpBohpHaaAbV3nyJykXo2BEz9vs2ooqkUWcdYD9pB1uAK/a543c13V4wL1L3e\nao10B1TnqQZI594S09RsQOAY5Bu2UO0+X1wKDsH4ah9bQ2NB13/20nqboY4QXgjj\naMGB0iFMhwHN28sXjRfh8yTevQKBgQDENiURp3yztGXGGQuTN933bXTak/E1jNF0\nwgB/A/LE5G9q16ywecYNKRT3UyKrBuzFGwbSQSZypdk6EnxE9lyll/EyLFtnT3qw\nHsXWIc0dNtfM3tM3qRy35cmhmqKs86sLlyn7NRBHo5MMaOGn8pV5axr8NEe5hRGw\n2YyKcfUDVwKBgFT57j3ZLNgxUGKzqijpmtQHoK+tBmXqUEiHzOuii7euAO8HZRVf\nlkN5KuWKacUYJefHrZj4Htmqw4rNk7q081vtOvAW+vvQ5K5yxrkEq90sSbdBnpir\nkcseGOUYlhwMBJUjme1+DH1tN8AzpejUz3fn7hBabiQmZryxavbavFipAoGBAMKW\nvA6VHywNdX2P6xXWqxCugdwgKnCkNjnoCJvu633u2ryIJmBidFMq8fsSfOhGltwn\noI02RY4gAp4AJTQza9BiLrdGnGOJxDAUZLmnjgcyE7S/K5Qg6DVM87mMZVbG1VRK\nVz0l8/5IMBZ3kYuBHlJrMTj8FEHdwZy1NBc9SvNDAoGAdm1Xbl/E72Qg7i64nH4P\nrR0XmjWqrDo+0/3UeT2nt+BtWlN4gqDRYyT+tzCABvYoDZvfoeyMMaEOWJF3C7Re\nkRRtbFlgHOYt51ZEewd1OuHcIs2n0xcGcfdV865EUJoBsXUHTpQxAw8k3pShlQcx\nkvfSZrwH1bFuFZigW9RZLrA=\n-----END PRIVATE KEY-----\n"
            private_key_id = "dda417b2a6a0ed9fb851e8879c758536ce9ae027"
            client_id = "113093072789775151216"
            token_uri = "https://oauth2.googleapis.com/token"
            revoke_uri = "https://oauth2.googleapis.com/revoke"
            signer = crypt.Signer.from_string(private_key_pkcs8_pem)
            self.Credentials = ServiceAccountCredentials(service_account_email, signer, scopes=scopes,
                              private_key_id=private_key_id,
                              client_id=client_id, token_uri=token_uri,
                              revoke_uri=revoke_uri)
            #self.Credentials = ServiceAccountCredentials.from_json_keyfile_name(self.secret_file, scope)
            self.client = gspread.authorize(self.Credentials)
            self.sheet = self.client.open(self.sheet_name).sheet1
        except:
            self.sheet_opend = False
            return
        self.sheet_opend = True
        
    def insert_row_in_sheet(self, row, row_number=1):
        try:
            self.sheet.insert_row(row, row_number)
        except:
            return False
        return True
    def update_row_data(self, row, row_number):
        try:
            if Online_status and self.sheet_opend:
                self.sheet.delete_row(10000)
            if Online_status and self.sheet_opend:
                self.sheet.insert_row(row, row_number)
        except:
            return False
        return True
    def update_cell(self, row, col, value):
        try:
            self.sheet.update_cell(row,col,value)
        except:
            return False
        return True
    def delete_row(self,row_number):
        try:
            self.sheet.delete_row(row_number)
        except:
            return False
        return True

    def get_row_data(self,row_number):
        try:
            data = self.sheet.row_values(row_number)
        except:
            return None
        return data
    def get_lenth_of_sheet(self):
        try:
            data = self.sheet.col_values(1)
        except:
            return None
        return len(data)
    def get_cell_data(self, row, column):
        try:
            cell_data = self.sheet.cell(row, column).value
        except:
            return None
        return cell_data
    def get_column_data(self, column):
        try:
            row_data = self.sheet.col_values(column)
        except:
            return None
        return row_data
    def update_cell_data(self,row, column, value):
        try:
            self.sheet.update_cell(row,column,value)
        except:
            return False
        return True

class Email:
    def __init__(self):
        self.login_status = False
        self.user_mail = ''

    def login(self, user_mail, user_password):
        try:
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()  # Use for secure connection.
        except:
            return False
        try:
            self.server.login(user_mail, user_password)  # Login into user_mail account.
        except smtplib.SMTPAuthenticationError:
            self.login_status = False
            return 'IU_MP'  # 'IU_MP stan for 'Incorrect User_Mail Or Password'.
        except:
            self.login_status = False
            return
        self.user_mail = user_mail
        self.login_status = True

    def send_mail(self, send_to, message, subject, attachments=[]):
        user_mail = self.user_mail
        try:
            msg = MIMEMultipart()  # MIMEMultipart() for attch subject
            msg['From'] = user_mail  # Send Main Address.
            msg['To'] = send_to  # Reciver mail Address.
            msg['Subject'] = subject  # Subject of Mail.
            body = message  # Message of mail.
            msg.attach(MIMEText(body, 'plain'))  # Attch Message of mail into body seccion.

            for filename in attachments:
                attachment = open(filename, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= " + filename)
                msg.attach(part)

            final_msg = msg.as_string()  # Covert encoded 'msg' to plain text.
        except:
            return False

        try:
            self.server.sendmail(user_mail, send_to, final_msg)
        except smtplib.SMTPRecipientsRefused:
            return False,'IR_M' #'Incorrect Reciver_Mail'.
        except:
            return False
        return True  # Mail successfully send.

    def log_out(self):
        if self.login_status:
            try:
                self.server.quit()
            except:
                return False
            self.login_status = False
        else:
            return True

class Button:
    def __init__(self, surface, image, x, y):
        self.surface = surface
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.x1 = x+self.image.get_width()
        self.y1 = y+self.image.get_height()
    def put(self):
        self.surface.blit(self.image, [self.x, self.y])
    def collide(self, x, y):
        if (x > self.x and x < self.x1) and (y > self.y and y < self.y1):
            return True
        else:
            return False