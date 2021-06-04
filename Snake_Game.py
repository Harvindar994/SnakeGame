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

class get_input:
    def __init__(self, surface, text, x, y, font_size, max_lenth, text_box_width, text_color, cursor_color):
        self.surface = surface
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.max_lenth = max_lenth
        self.text_box_width = text_box_width
        self.text_color = text_color
        self.cursor_color = cursor_color
        self.caption_font_file = 'Font/Kollektif.ttf'
        self.font_file = 'Font/Gidole-Regular.otf'
        self.text_box_height = out_text_file(self.surface, 'Q', self.font_size, 100, 100, self.text_color, self.font_file, True)
        self.text_box_height = self.text_box_height.get_height() + 2
        self.lenth = len(text)
        self.Dec_value = 0
        self.Flag = False
        self.clock = pygame.time.Clock()
        self.count = 0
        self.count_2 = 0
        self.cursor_flag = False
        self.select_flag = False
        self.spcial_car = []
        self.text_img = out_text_file(self.surface, '', self.font_size, 100, 100, self.text_color, self.font_file, True)

    def put_text(self):
        self.surface.blit(self.text_img, [self.x+2, self.y+1])

    def get_tex_box_size_image_of_text(self):
        self.font_file = 'Font/Gidole-Regular.otf'
        img = out_text_file(self.surface, self.text, self.font_size, 100, 100, self.text_color, self.font_file, True)
        Lenth = 20
        if img.get_width() > self.text_box_width:
            while True:
                temp = self.text[0:Lenth]
                Lenth += 1
                img = out_text_file(self.surface, temp, self.font_size, 100, 100, self.text_color, self.font_file,True)
                if not img.get_width() < self.text_box_width - 14:
                    break
            self.text_img = img
            return img
        else:
            self.text_img = img
            return img

    def get_tex_box_size_image_of_password(self):
        self.font_file = 'Font/ProFontWindows.ttf'
        password = ''
        for e in self.text:
            password += '*'
        img = out_text_file(self.surface, password, self.font_size, 100, 100, self.text_color, self.font_file, True)
        Lenth = 20
        if img.get_width() > self.text_box_width:
            while True:
                temp = password[0:Lenth]
                Lenth += 1
                img = out_text_file(self.surface, temp, self.font_size, 100, 100, self.text_color, self.font_file,True)
                if not img.get_width() < self.text_box_width - 14:
                    break
            self.text_img = img
            return img
        else:
            self.text_img = img
            return img

    def input_text(self,event_list):
        self.font_file = 'Font/Gidole-Regular.otf'
        for event in event_list:
            if event.type == pygame.KEYUP:
                if event.key == 


                pygame.K_BACKSPACE:
                    self.Flag = False
                    self.count = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.lenth = 0
                    self.text = ""
                if event.key == pygame.K_BACKSPACE and self.lenth > 0:
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    else:
                        self.lenth -= 1
                        self.text = self.text[0:self.lenth]
                        self.Flag = True
                if (event.unicode >= 'a' and event.unicode <= 'z') or (event.unicode >= 'A' and event.unicode <= 'Z'):
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    if self.lenth < self.max_lenth:
                        key = event.unicode
                        self.text += key
                        self.lenth += 1
                    else:
                        pass
                if event.unicode in self.spcial_car:
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    if self.lenth < self.max_lenth:
                        key = event.unicode
                        self.text += key
                        self.lenth += 1
                if event.key == 99 and self.lenth > 0 and (event.mod == 64 or event.mod == 128):
                    if self.select_flag:
                        clipboard.copy(self.text)
                if event.key == 118 and (event.mod == 64 or event.mod == 128):
                        text = clipboard.paste()
                        if len(text)!=0:
                            if len(text)>self.max_lenth:
                                text = text[0:self.max_lenth]
                        self.text = text
                        self.lenth = len(text)
                if not (event.key == 305 or event.key == 306):
                    self.select_flag = False
                if event.key == 97 and self.lenth > 0 and (event.mod == 64 or event.mod == 128):
                    self.select_flag = True


        if self.Flag and self.count < 10:
            self.count += 1
        elif self.Flag and self.lenth > 0:
            self.lenth -= 1
            self.text = self.text[0:self.lenth]

        self.temp = self.text
        if self.select_flag:
            img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True, (41, 169, 234))
        else:
            img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True)
        if img.get_width() > self.text_box_width:
            while True:
                self.temp = self.text[self.lenth - self.Dec_value::]
                self.Dec_value += 1
                if self.select_flag:
                    img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True,(41, 169, 234))
                else:
                    img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True)
                if not img.get_width() < self.text_box_width - 14:
                    break
        if self.count_2 < 10:
            self.cursor_flag = True
            self.count_2 += 1
        elif self.count_2 < 20:
            self.cursor_flag = False
            self.count_2 += 1
        else:
            self.count_2 = 0

        self.Dec_value = 0
        self.surface.blit(img, (self.x + 2, self.y + 1))
        if self.cursor_flag:
            pygame.draw.line(self.surface, self.cursor_color, [self.x + 5 + img.get_width(), self.y + 2],[self.x + 5 + img.get_width(), self.y + self.text_box_height - 2])

    def input_numbers(self,event_list):
        self.font_file = 'Font/Gidole-Regular.otf'
        for event in event_list:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.Flag = False
                    self.count = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.lenth = 0
                    self.text = ""
                if event.key == pygame.K_BACKSPACE and self.lenth > 0:
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    else:
                        self.lenth -= 1
                        self.text = self.text[0:self.lenth]
                        self.Flag = True
                if (event.unicode >= '0' and event.unicode <= '9'):
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    if self.lenth < self.max_lenth:
                        key = event.unicode
                        self.text += key
                        self.lenth += 1
                    else:
                        pass
                if event.unicode in self.spcial_car:
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    if self.lenth < self.max_lenth:
                        key = event.unicode
                        self.text += key
                        self.lenth += 1
                if event.key == 99 and self.lenth > 0 and (event.mod == 64 or event.mod == 128):
                    if self.select_flag:
                        clipboard.copy(self.text)
                if event.key == 118 and (event.mod == 64 or event.mod == 128):
                        text = clipboard.paste()
                        if len(text)!=0:
                            if len(text)>self.max_lenth:
                                text = text[0:self.max_lenth]
                        self.text = text
                        self.lenth = len(text)
                if not (event.key == 305 or event.key == 306):
                    self.select_flag = False
                if event.key == 97 and self.lenth > 0 and (event.mod == 64 or event.mod == 128):
                    self.select_flag = True


        if self.Flag and self.count < 10:
            self.count += 1
        elif self.Flag and self.lenth > 0:
            self.lenth -= 1
            self.text = self.text[0:self.lenth]

        self.temp = self.text
        if self.select_flag:
            img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True, (41, 169, 234))
        else:
            img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True)
        if img.get_width() > self.text_box_width:
            while True:
                self.temp = self.text[self.lenth - self.Dec_value::]
                self.Dec_value += 1
                if self.select_flag:
                    img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True,(41, 169, 234))
                else:
                    img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True)
                if not img.get_width() < self.text_box_width - 14:
                    break
        if self.count_2 < 10:
            self.cursor_flag = True
            self.count_2 += 1
        elif self.count_2 < 20:
            self.cursor_flag = False
            self.count_2 += 1
        else:
            self.count_2 = 0

        self.Dec_value = 0
        self.surface.blit(img, (self.x + 2, self.y + 1))
        if self.cursor_flag:
            pygame.draw.line(self.surface, self.cursor_color, [self.x + 5 + img.get_width(), self.y + 2],[self.x + 5 + img.get_width(), self.y + self.text_box_height - 2])

    def input_password(self,event_list):
        self.font_file = 'Font/ProFontWindows.ttf'
        for event in event_list:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.Flag = False
                    self.count = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.lenth = 0
                    self.text = ""
                if event.key == pygame.K_BACKSPACE and self.lenth > 0:
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    else:
                        self.lenth -= 1
                        self.text = self.text[0:self.lenth]
                        self.Flag = True
                if (event.unicode >= 'a' and event.unicode <= 'z') or (event.unicode >= 'A' and event.unicode <= 'Z'):
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    if self.lenth < self.max_lenth:
                        key = event.unicode
                        self.text += key
                        self.lenth += 1
                    else:
                        pass
                if event.unicode in self.spcial_car:
                    if self.select_flag:
                        self.lenth = 0
                        self.text = ""
                    if self.lenth < self.max_lenth:
                        key = event.unicode
                        self.text += key
                        self.lenth += 1
                if event.key == 99 and self.lenth > 0 and (event.mod == 64 or event.mod == 128):
                    if self.select_flag:
                        clipboard.copy(self.text)
                if event.key == 118 and (event.mod == 64 or event.mod == 128):
                    text = clipboard.paste()
                    if len(text) != 0:
                        if len(text) > self.max_lenth:
                            text = text[0:self.max_lenth]
                    self.text = text
                    self.lenth = len(text)
                if not (event.key == 305 or event.key == 306):
                    self.select_flag = False
                if event.key == 97 and self.lenth > 0 and (event.mod == 64 or event.mod == 128):
                    self.select_flag = True

        if self.Flag and self.count < 10:
            self.count += 1
        elif self.Flag and self.lenth > 0:
            self.lenth -= 1
            self.text = self.text[0:self.lenth]

        self.temp = ''
        for e in self.text:
            self.temp = self.temp + '*'
        if self.select_flag:
            img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True, (41, 169, 234))
        else:
            img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True)
        if img.get_width() > self.text_box_width:
            while True:
                self.temp = self.text[self.lenth - self.Dec_value::]
                self.temp = len(self.temp)*'*'
                self.Dec_value += 1
                if self.select_flag:
                    img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True,(41, 169, 234))
                else:
                    img = out_text_file(self.surface, self.temp, self.font_size, 100, 100, self.text_color, self.font_file, True)
                if not img.get_width() < self.text_box_width - 14:
                    break
        if self.count_2 < 10:
            self.cursor_flag = True
            self.count_2 += 1
        elif self.count_2 < 20:
            self.cursor_flag = False
            self.count_2 += 1
        else:
            self.count_2 = 0

        self.Dec_value = 0
        self.surface.blit(img, (self.x + 2, self.y + 1))
        if self.cursor_flag:
            pygame.draw.line(self.surface, self.cursor_color, [self.x + 5 + img.get_width(), self.y + 2],[self.x + 5 + img.get_width(), self.y + self.text_box_height - 2])

class Setting:
    def __init__(self):
        self.Music_Valume = 0.0390625
        self.Music_Button_x = 281
        self.Sound_button_x = 530
        self.Sound_valume = 1.0
        self.online_score = False
        self.feedback_sended = False
        self.login_status = False
        self.Name = ""
        self.Email = ""
        self.Password = ""
        self.PC_name = ""
        self.Mac_Address = ""
        self.IP_Address = ""
        self.ISP = ""
        self.Country = ""
        self.State = ""
        self.City = ""
        self.DOCA = ""

    def check_setting(self, type=0):
        try:
            fp = open("Setting.ini",'rb')
        except FileNotFoundError:
            data = Setting()
            if type == 1 or type == 0:
                set_valuem(Background_sound, data.Music_Valume)
            if type == 2 or type == 0:
                set_valuem(Eat_Food_sound, data.Sound_valume)
                set_valuem(Menu_sound, data.Sound_valume)
                set_valuem(Error_sound, data.Sound_valume)
                set_valuem(Welcome_sound, data.Sound_valume)
                set_valuem(Show_extra_food_sound, data.Sound_valume)
                set_valuem(Notify_sound, data.Sound_valume)
                set_valuem(Crash_sound, data.Sound_valume)
                set_valuem(Slide_sound, data.Sound_valume)
            return data
        try:
            data = pickle.load(fp)
        except:
            fp.close()
            data = Setting()
            if type == 1 or type == 0:
                set_valuem(Background_sound, data.Music_Valume)
            if type == 2 or type == 0:
                set_valuem(Eat_Food_sound, data.Sound_valume)
                set_valuem(Menu_sound, data.Sound_valume)
                set_valuem(Error_sound, data.Sound_valume)
                set_valuem(Welcome_sound, data.Sound_valume)
                set_valuem(Show_extra_food_sound, data.Sound_valume)
                set_valuem(Notify_sound, data.Sound_valume)
                set_valuem(Crash_sound, data.Sound_valume)
                set_valuem(Slide_sound, data.Sound_valume)
            return data

        if type == 1 or type ==0:
            set_valuem(Background_sound, data.Music_Valume)
        if type == 2 or type ==0:
            set_valuem(Eat_Food_sound, data.Sound_valume)
            set_valuem(Menu_sound, data.Sound_valume)
            set_valuem(Error_sound, data.Sound_valume)
            set_valuem(Welcome_sound, data.Sound_valume)
            set_valuem(Show_extra_food_sound, data.Sound_valume)
            set_valuem(Notify_sound, data.Sound_valume)
            set_valuem(Crash_sound, data.Sound_valume)
            set_valuem(Slide_sound, data.Sound_valume)
        fp.close()
        return data

    def update_setting(self):
        try:
            fp = open("Setting.ini",'wb')
        except:
            return False
        pickle.dump(self,fp)
        fp.close()
        return True


class online_score_record:
    snake = 10
    Getting_data = False
    def __int__(self):
        self.High_score = 0
        self.Name = ''
        self.Email = ''

    def update_score(self, name, score, Email):
        while online_score_record.Getting_data:
            pass
        if not score > self.get_High_score():
            return False
        if not (len(name)>0 and len(Email)>0):
            return False
        if not (type(score) == int):
            try:
                score = int(score)
            except:
                return False
        try:
            fp = open("online_record.rc", "wb")
        except:
            return 0
        self.High_score = score
        self.Name = name
        self.Email = Email
        pickle.dump(self, fp)
        fp.close()

    def get_High_score(self):
        online_score_record.Getting_data = True
        try:
            fp = open("online_record.rc", "rb")
            data = pickle.load(fp)
            fp.close()
        except:
            online_score_record.Getting_data = False
            return 0
        online_score_record.Getting_data = False
        return data.High_score
    def get_High_score_name(self):
        online_score_record.Getting_data = True
        try:
            fp = open("online_record.rc", "rb")
            data = pickle.load(fp)
            fp.close()
        except:
            online_score_record.Getting_data = False
            return ""
        online_score_record.Getting_data = False
        return data.Name
    def get_High_score_email(self):
        online_score_record.Getting_data = True
        try:
            fp = open("online_record.rc", "rb")
            data = pickle.load(fp)
            fp.close()
        except:
            online_score_record.Getting_data = False
            return ""
        online_score_record.Getting_data = False
        return data.Email


class score_record:
    snake  = 10
    updating_data = False
    def __int__(self):
        self.High_score = 0

    def update_score(self, score):
        score_record.updating_data = False
        high_score = self.get_High_score()
        score_record.updating_data = True
        try:
            if score > high_score:
                try:
                    fp = open("record.rc","wb")
                except:
                    score_record.updating_data = False
                    return 0
                self.High_score = score
                pickle.dump(self, fp)
                fp.close()
                score_record.updating_data = False
                return score
            else:
                score_record.updating_data = False
                return high_score
        except:
            score_record.updating_data = False
            return high_score

    def get_High_score(self):
        while score_record.updating_data:
            pass
        try:
            fp = open("record.rc","rb")
            data = pickle.load(fp)
            fp.close()
        except:
            return 0
        return  data.High_score


#-------------------------------------------Loding Sound Files--------------------------
Background_sound = load_sound("Sound/background_sound.wav")
Eat_Food_sound = load_sound("Sound/Eat_food_sound.wav")
Menu_sound = load_sound("Sound/Menu sound.wav")
Star_sound = load_sound("Sound/Star_sound.wav")
Click_sound = load_sound("Sound/Click_sound.wav")
Error_sound = load_sound("Sound/Error_sound.wav")
Welcome_sound = load_sound("Sound/Welcome_sound.wav")
Show_extra_food_sound = load_sound("Sound/Show_extra_food_sound.wav")
Notify_sound = load_sound("Sound/Notify_sound.wav")
Crash_sound = load_sound("Sound/Crash_sound.wav")
Slide_sound = load_sound("Sound/Swing_sound.wav")

#------------------------------------Loding Image Files-----------------------------
About_Img = pygame.image.load("Image\About.png")
Menu_img = pygame.image.load("Image\Menu_temp.png")
main_menu_img = pygame.image.load("Image\Menu.png")
play_ground = pygame.image.load("Image\Play_ground.png")
game_over_img = pygame.image.load("Image/game_over.png")
icon  = pygame.image.load("Image/icon.png")
setting_img = pygame.image.load("Image/Setting.png")
Send_feedback = pygame.image.load("Image/Feedback.png")
create_ac_img = pygame.image.load('Image/Create_account.png')
Login_img = pygame.image.load("Image/Login.png")
line  = pygame.image.load('Image/line.png')
Menu_bk = pygame.image.load('Image/Menu_bk.png')

#----------------------------------Working On Game Window---------------------
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake Game")
GameWindow = pygame.display.set_mode((692, 389))


#---------------------------------Colors-----------------------------------
Light_Pink = (255, 172, 182)
white = (255, 255, 255)
light_black = (43, 43, 43)
black = (0, 0, 0)
light_blue = (0, 135, 255)
Yellow = (248, 207, 44)
Red = (255, 23, 68)
orange = (255, 98, 11)
light_green = (114, 252, 56)

#---------------------------------Global Variables-----------------------------------
Close_game = False
Start_x = 346
Start_y = 38
Diffrence = 117
Hight = 270
Width = 78
Mouse_x = 0
Mouse_y = 0
Setting_obj = Setting()
clock = pygame.time.Clock()
Sheet = None
Gmail = Email()
Online_status = False
IP_ADDRESS = None
MAC_ADDRESS = None
COMPUTER_NAME = None
ONLINE_DATE = None
Game_Version = "1.0.0"


#---------------------------------------Google Sheets-------------------------
Jeson_secret_file = 'Feedback.json'
Feedback_sheet_Name = 'FeedBack_Snake_Game_1.0.0'
User_account_sheet_name = 'User Accounts'
High_Score_Sheet_name = 'High Score'
Service_Email_sheet_name = 'Service Email'
Service_Email_sheet = google_sheet(Service_Email_sheet_name, Jeson_secret_file)
Online_score_sheet = google_sheet(High_Score_Sheet_name, Jeson_secret_file)
Feedback_sheet = google_sheet(Feedback_sheet_Name,Jeson_secret_file)
User_account_sheet = google_sheet(User_account_sheet_name, Jeson_secret_file)

#----------------------------------------Check Setting------------------------
Setting_obj.check_setting()

#----------------------------------------Global Flags to Control Threads-------------------------
controling_thread = None

##----------------------------------------Global Flags to Controling-------------------------
Feedback_sending = True
OTP_sended = False


def get_online_date():
    #from urllib.request import urlopen
    try:
        res = urlopen('http://just-the-time.appspot.com/')
        time_str = str(res.read().strip())
        date = time_str[2:12]
    except:
        return None
    return date

def get_ip_address_with_details():
    #import json
    #from urllib.request import urlopen
    url = 'http://ipinfo.io/json'
    try:
        response = urlopen(url)
        data = json.load(response)
    except:
        return None
    return data

def get_computer_name():
    #import socket
    try:
        name = socket.gethostname()
    except:
        return None
    return name

def get_mac_address():
    #import uuid
    #import re
    try:
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except:
        return
    return mac

def checkOnlineState():
    try:
        socket.create_connection(("www.google.com",80))
        return True
    except OSError:
        return False
    except:
        return False


def custom_out_text(surface, text, x, x1, y, color, size, f_file = "Font/Kollektif.ttf"):
    text_img = out_text_file(surface, text, size, 0, 0, color, f_file, True)
    put_point_x = x + ((x1 - x) // 2)
    put_point_x = put_point_x - (text_img.get_width() // 2)
    surface.blit(text_img, [put_point_x, y])

def stop_sound(sound_file):
    pygame.mixer.Sound.stop(sound_file)

def caption(text, x, y, window_width = 692, window_height = 389, bk_color = (255, 255, 255), border_color = (43, 43, 43)):
    difrence_between_m_y = 16
    difrence_between_m_x = 7
    text_img = out_text_file(GameWindow, text, 12, 0, 0,black, "Font\DroidSansMono.ttf", True)
    rect_width = text_img.get_width()+6
    rect_height = text_img.get_height()+4
    rect_x = x+difrence_between_m_x
    rect_y = y+difrence_between_m_y
    if (rect_y+rect_height > window_height) and (rect_x+rect_width > window_width):
        rect_x = x-rect_width
        rect_y = y-rect_height
    if rect_x+rect_width > window_width:
        rect_x = rect_x-rect_width
    if rect_y+rect_height > window_height:
        rect_x = x
        rect_y = y-rect_height

    pygame.draw.rect(GameWindow, bk_color,[rect_x, rect_y, rect_width, rect_height])
    pygame.draw.rect(GameWindow, border_color, [rect_x, rect_y, rect_width, rect_height], 1)
    GameWindow.blit(text_img, [rect_x+3, rect_y+2]) #10, 5


def online_work_handler():
    global Online_score_sheet
    global Setting_obj
    global Online_status
    global User_account_sheet
    global Feedback_sheet, Gmail
    global IP_ADDRESS
    global MAC_ADDRESS
    global COMPUTER_NAME
    global ONLINE_DATE
    global controling_thread
    global Service_Email_sheet
    score_thread_status = False
    online_work_thread_status = False
    Setting_obj = Setting_obj.check_setting()
    controling_thread = True
    Online_score_thread = threading.Thread(target=online_score_handler)
    online_sheet_handler = threading.Thread(target=google_sheet_handler)
    while controling_thread:
        Online_status = checkOnlineState()
        if not Online_status:
            Online_score_sheet.sheet_opend = False
            Feedback_sheet.sheet_opend = False
            User_account_sheet.sheet_opend = False
            Service_Email_sheet.sheet_opend = False
            Gmail.login_status = False
            COMPUTER_NAME = None
            MAC_ADDRESS = None
            ONLINE_DATE = None
            IP_ADDRESS = None
        else:
            if not online_work_thread_status:
                online_sheet_handler.start()
                online_work_thread_status = True
            if not score_thread_status:
                if Setting_obj.login_status and Setting_obj.online_score:
                    Online_score_thread.start()
                    score_thread_status = True
        """print("Online_score_Scheet_opend : ", Online_score_sheet.sheet_opend)
        print("FeedBack sheet Status : ", Feedback_sheet.sheet_opend)
        print("User account sheet status : ", User_account_sheet.sheet_opend)
        print("Online Score Scheet  : ", Online_score_sheet.sheet_opend)
        print("IP Address : ", IP_ADDRESS)
        print("MAC ADDDRESS : ", MAC_ADDRESS)
        print("ONLINE DATE : ", ONLINE_DATE)
        print("COMPUTER NAME : ", COMPUTER_NAME)"""
    else:
        Online_score_sheet.sheet_opend = False
        Feedback_sheet.sheet_opend = False
        User_account_sheet.sheet_opend = False
        Online_score_sheet.sheet_opend = False
        COMPUTER_NAME = None
        MAC_ADDRESS = None
        ONLINE_DATE = None
        IP_ADDRESS = None


def online_score_handler():
    global Setting_obj
    global Online_score_sheet
    global Local_high_score
    global Online_High_score
    global Online_High_score_email
    global Online_High_score_name
    global Playing_Status
    global controling_thread
    Clock = pygame.time.Clock()
    Online_score = online_score_record()
    local_score = score_record()
    Setting_obj = Setting_obj.check_setting()
    global Online_score_handler_number
    while controling_thread:
        if Setting_obj.login_status and Setting_obj.online_score:
            if Online_status:
                if not Online_score_sheet.sheet_opend:
                    Online_score_sheet.open_sheet()
                    continue
                elif Online_status and Online_score_sheet.sheet_opend and controling_thread and Setting_obj.login_status and Setting_obj.online_score:
                    data = Online_score_sheet.get_row_data(2)
                    sheet_lenth = False
                    if Playing_Status:
                        local_high_score = Local_high_score
                    else:
                        local_high_score = local_score.get_High_score()

                    if type(data) == list:
                        if sheet_lenth:
                            if local_high_score > 0:
                                if Online_status and Online_score_sheet.sheet_opend and controling_thread and Setting_obj.login_status and Setting_obj.online_score:
                                    row = [local_high_score, Setting_obj.Name, Setting_obj.Email, Setting_obj.Password,ONLINE_DATE]
                                    Online_score_sheet.update_row_data(row, 2)
                                    Online_High_score = local_high_score
                                    Online_High_score_name = Setting_obj.Name
                                    Online_High_score_email = Setting_obj.Email
                                else:
                                    Online_score_sheet.sheet_opend = False
                                    continue
                                if Setting_obj.login_status and Setting_obj.online_score:
                                    Online_score.update_score(Setting_obj.Name, local_high_score, Setting_obj.Email)
                                else:
                                    Online_score_sheet.sheet_opend = False
                                    continue
                            continue
                        elif len(data) == 5:
                            if local_high_score > int(data[0]):
                                if Online_status and Online_score_sheet.sheet_opend and controling_thread and Setting_obj.login_status and Setting_obj.online_score:
                                    row = [local_high_score, Setting_obj.Name, Setting_obj.Email, Setting_obj.Password,ONLINE_DATE]
                                    Online_score_sheet.update_row_data(row, 2)
                                    Online_High_score = local_high_score
                                    Online_High_score_name = Setting_obj.Name
                                    Online_High_score_email = Setting_obj.Email
                                else:
                                    Online_score_sheet.sheet_opend = False
                                    continue
                                if Setting_obj.login_status and Setting_obj.online_score:
                                    Online_score.update_score(Setting_obj.Name, local_high_score, Setting_obj.Email)
                                else:
                                    Online_score_sheet.sheet_opend = False
                                    continue
                            else:
                                Online_score.update_score(data[1], int(data[0]), data[2])
                                Online_High_score = int(data[0])
                                Online_High_score_name = data[1]
                                Online_High_score_email = data[2]
                            continue
                    else:
                        Online_score_sheet.sheet_opend = False
                        continue
                else:
                    Online_score_sheet.sheet_opend = False
                    continue


def google_sheet_handler():
    global Setting_obj
    global User_account_sheet
    global Online_status
    global Feedback_sheet, Gmail
    global IP_ADDRESS
    global MAC_ADDRESS
    global COMPUTER_NAME
    global ONLINE_DATE
    global controling_thread
    email_address = ''
    password = ''
    Setting_obj = Setting_obj.check_setting()

    while controling_thread:
        if Online_status:
            ONLINE_DATE = get_online_date()
            if not Feedback_sheet.sheet_opend and controling_thread and Online_status:
                Feedback_sheet.open_sheet()
            if not Service_Email_sheet.sheet_opend and controling_thread and Online_status:
                Service_Email_sheet.open_sheet()
            if not Gmail.login_status and Service_Email_sheet.sheet_opend and controling_thread and Online_status:
                data = Service_Email_sheet.get_row_data(2)
                if type(data)==list and len(data)>=2:
                    email_address = data[0]
                    password = data[1]
                    if email_address != '' and password != '' and controling_thread and Online_status:
                        Gmail.login(email_address, password)
            if not User_account_sheet.sheet_opend and controling_thread and Online_status:
                User_account_sheet.open_sheet()
            if IP_ADDRESS==None and controling_thread and Online_status:
                IP_ADDRESS = get_ip_address_with_details()
            if MAC_ADDRESS==None or MAC_ADDRESS=='' and controling_thread and Online_status:
                MAC_ADDRESS = get_mac_address()
            if COMPUTER_NAME==None or COMPUTER_NAME=='' and controling_thread and Online_status:
                COMPUTER_NAME = get_computer_name()
        else:
            Feedback_sheet.sheet_opend = False
            User_account_sheet.sheet_opend = False
            Online_score_sheet.sheet_opend = False
            COMPUTER_NAME = None
            MAC_ADDRESS = None
            ONLINE_DATE = None
            IP_ADDRESS = None
            email_address = ''
            password = ''
            try:
                Gmail.log_out()
                Gmail.login_status = False
            except:
                pass

def put_img(surface, file, x, y, display_or_nor=True):
    try:
        image = pygame.image.load(file)
    except:
        return 0
    if display_or_nor:
        try:
            surface.blit(image, [x, y])
        except:
            return 0
    return image.get_width(), image.get_height(), image

def open_url(url):
    import webbrowser
    try:
        webbrowser.get('chrome').open_new(url)
    except:
        try:
            webbrowser.get('firefox').open_new_tab(url)
        except:
            try:
                webbrowser.open(url, new=1)
            except:
                return False
    return True


#------------------ Temp Function to define screen objects ----------------------
def selecter(x,y,mouse_x,mouse_y,color=white):
    pygame.draw.rect(GameWindow,color,[x,y,mouse_x-x,mouse_y-y],1)
def define_pos(image,x,y):
    flag = False
    x = 0
    y = 0
    Mouse_x = 0
    Mouse_y = 0
    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if flag:
                    print("Mouse X : ", Mouse_x)
                    print("Mouse Y : ", Mouse_y)
                    flag = False
                else:
                    flag = True
                    print("POS X : ", x)
                    print("POS Y : ", y)

        GameWindow.blit(image, [0, 0])
        if flag:
            selecter(x, y, Mouse_x, Mouse_y, orange)
        pygame.display.update()