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

def msg_box(surface,msg):
    global Mouse_x,Mouse_y
    pygame.image.save(surface, 'temp.png')
    pop_image = pygame.image.load("Image/popup_msg.png")
    close_white = pygame.image.load("Image/white_close.png")
    close_orange = pygame.image.load("Image/orange_close.png")
    bk_img = pygame.image.load("temp.png")
    font_size = 20
    Stop_font_adjustment = False
    msg = msg.split(',')
    close_msg = False
    step = 25
    while not Stop_font_adjustment:
        Max_width_line = 0
        center_x = 350
        center_y = 188
        hight = 0
        width = 0
        x = 346
        y = 194
        msg_img = []
        for m in msg:
            img = out_text_file(surface, m, font_size, 0, 0, white, "Font/DroidSansMono.ttf", True)
            temp = img.get_width()
            if temp > Max_width_line:
                Max_width_line = temp
            msg_img.append(img)

        text_pos = 200
        if len(msg)%2!=0:
            height = msg_img[0].get_height()//2
            text_pos -= height

        msg_lenth = len(msg)
        if msg_lenth>1:
            half = msg_lenth//2
            while half!=0:
                text_pos -= step
                half -= 1
        elif msg_lenth==1:
            text_pos = text_pos - (msg_img[0].get_height()//2)

        temp = len(msg_img)
        if text_pos+(temp*step)>273:
            font_size -= 2
            step -= 2
            continue
        elif 174+Max_width_line > 518 or 518-Max_width_line < 174:
            font_size -= 2
            continue
        Stop_font_adjustment = True

    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Mouse_x >= 490 and Mouse_x <= 490 + 16 and Mouse_y >= 140 and Mouse_y <= 156:
                    close_msg = True
        bgimg = pygame.transform.scale(pop_image, (width, hight)).convert_alpha()
        surface.blit(bk_img, [0, 0])
        surface.blit(bgimg, [x, y])
        if not close_msg:
            if width<pop_image.get_width():
                hight += 30 #22 # 22
                width += 56 #44 # 40
                x -= 28 #22, 11 #20, 11
                y -= 15
            else:
                if Mouse_x >= 490 and Mouse_x<=490+16 and Mouse_y >= 140 and Mouse_y <= 156:
                    surface.blit(close_orange, [490,140])
                else:
                    surface.blit(close_white,[490,140])
                temp = text_pos
                for text in msg_img:
                    img_width = text.get_width()
                    surface.blit(text, [center_x-(img_width//2), temp])
                    temp += step
        else:
            if width>0:
                hight -= 30 #22
                width -= 56 #44, 40
                x += 28 #22, 11, #20, 11
                y += 15
            else:
                return
        pygame.display.update()


def collide(m_x,m_y, x, y, x1, y1):
    if (m_x > x and m_x < x1) and (m_y > y and m_y < y1):
        return True
    else:
        return False
def send_otp(Email,otp,Name,type = 0):
    global OTP_sended
    global Gmail
    OTP_sended = False
    if type == 0:
        Email_msg = "Hi "+Name+",\n\nYour OTP is : "+str(otp)+"\nDo not share this OTP with another.\n\nShare, Support, Subscribe!!!\nYoutube: https://www.youtube.com/channel/UCCEBsUxSW7PyyCYLw8cyhvA\nTwitter:  https://twitter.com/brightgoal_in\nFacebook Page: https://www.facebook.com/brightgoal.in.Education\nFacebook Myself: https://www.facebook.com/harvindar.brightgoal\nInstagram: https://www.instagram.com/brightgoal.in/\nWebsite: https://www.brightgoal.in/\n\nPowered By : Harvindar Singh\nVisit on Store for More Product : https://www.instamojo.com/Brightgoal\n"
        re = Gmail.send_mail(Email,Email_msg,'Snake Game OTP verification.')
    elif type == 1:
        Email_msg = "Your OTP is : " + str(otp) + "\nDo not share this OTP with another.\n\nShare, Support, Subscribe!!!\nYoutube: https://www.youtube.com/channel/UCCEBsUxSW7PyyCYLw8cyhvA\nTwitter:  https://twitter.com/brightgoal_in\nFacebook Page: https://www.facebook.com/brightgoal.in.Education\nFacebook Myself: https://www.facebook.com/harvindar.brightgoal\nInstagram: https://www.instagram.com/brightgoal.in/\nWebsite: https://www.brightgoal.in/\n\nPowered By : Harvindar Singh\nVisit on Store for More Product : https://www.instamojo.com/Brightgoal\n"
        re = Gmail.send_mail(Email, Email_msg, 'Snake Game Reset Password.')
    if re== 'IR_M':
        OTP_sended = re
    elif re == True:
        OTP_sended = True

def email_already_reg(email):
    global User_account_sheet, Online_status
    if User_account_sheet.sheet_opend and Online_status:
        lenth = User_account_sheet.get_lenth_of_sheet()
        cloumn = 2
        row = 1
        if type(lenth)==int:
            if lenth >= 1:
                while row<=lenth:
                    if User_account_sheet.sheet_opend and Online_status:
                        data = User_account_sheet.get_cell_data(row, cloumn)
                        if data==email:
                            return True, row, cloumn
                        row += 1
                    else:
                        break
    return False, None, None


def check_email_and_password(email, password):
    global User_account_sheet
    if User_account_sheet.sheet_opend and Online_status:
        lenth = User_account_sheet.get_lenth_of_sheet()
        row = 1
        if type(lenth) == int:
            if lenth >= 1:
                while row <= lenth:
                    if User_account_sheet.sheet_opend and Online_status:
                        data = User_account_sheet.get_row_data(row)
                        if email in data:
                            if password in data and len(data)==11:
                                return True, data
                            else:
                                break
                        row += 1
                    else:
                        break
    return False, []

def Reset_password(email = ''):
    global GameWindow
    global Mouse_y, Mouse_x
    global white
    global light_green
    global User_account_sheet
    Red = (254, 55, 14)
    reset_img = pygame.image.load("Image/Reset_password.png")
    close_white = Button(GameWindow, "Image/close_white.png", 17, 17)
    close_green = Button(GameWindow, "Image/close_green.png", 17, 17)
    view_pass_white = Button(GameWindow, "Image/view_pass_white.png", 568, 236)
    view_pass_green = Button(GameWindow, "Image/view_pass_green.png", 568, 236)
    hide_pass_white = Button(GameWindow, "Image/hide_pass_white.png", 568, 236)
    hide_pass_green = Button(GameWindow, "Image/hide_pass_green.png", 568, 236)
    Submit_green = Button(GameWindow, "Image/Submit_green.png", 275, 300)
    Submit_black = Button(GameWindow, "Image/Submit_black.png", 275, 300)
    Input_Email = False
    Input_Password = False
    Input_Otp = False
    Email = get_input(GameWindow, email, 163, 114, 20, 450, 390, white, white)
    Email.get_tex_box_size_image_of_text()
    OTP = get_input(GameWindow, '', 163, 172, 20, 6, 390, white, white)
    Password = get_input(GameWindow, '', 163, 233, 20, 40, 390, white, white)
    Email.spcial_car = ['@', '.', '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '#', '$', '%', '&',
                        "'", '*', '+', '/', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';', '<',
                        '>', '[', '\\', ']']
    Password.spcial_car = ['@', '.', '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '#', '$', '%',
                           '&',
                           "'", '*', '+', '/', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';',
                           '<',
                           '>', '[', '\\', ']']
    event_list = []
    Email_caption = get_input(GameWindow, "Registered Email", 163, 114, 20, 450, 390, white, white)
    Otp_caption = get_input(GameWindow, 'OTP', 163, 172, 20, 6, 390, white, white)
    Password_caption = get_input(GameWindow, 'New Password', 163, 233, 20, 40, 390, white, white)
    Email_caption.get_tex_box_size_image_of_text()
    Password_caption.get_tex_box_size_image_of_text()
    Otp_caption.get_tex_box_size_image_of_text()
    show_password = False
    show_email_caption = True
    show_password_caption = True
    show_otp_caption = True
    OTP_PASS = -1
    otp_send_on = ''
    otp_sended = False
    row = -1
    col = -1
    status = False
    Verification = False
    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                event_list.append(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if close_green.collide(Mouse_x, Mouse_y):
                        return
                    if collide(Mouse_x, Mouse_y, 74, 112, 620, 150):
                        Input_Email = True
                        Input_Password = False
                        Input_Otp = False
                        show_email_caption = False
                        show_password_caption = True
                        show_otp_caption = True

                    if collide(Mouse_x, Mouse_y, 74, 170, 620, 212):
                        Input_Password = False
                        Input_Email  = False
                        Input_Otp = True
                        show_email_caption = True
                        show_password_caption = True
                        show_otp_caption = False

                    if collide(Mouse_x, Mouse_y, 74, 231, 620, 273):
                        Input_Email = False
                        Input_Password = True
                        Input_Otp = False
                        show_email_caption = True
                        show_password_caption = False
                        show_otp_caption = True

                    if collide(Mouse_x, Mouse_y, 244, 350, 477, 369):
                        create_account()
                    if Submit_green.collide(Mouse_x, Mouse_y):
                        if validate_email(Email.text):
                            if str(OTP_PASS) == OTP.text:
                                if validate_password(Password.text,8):
                                    Verification = True
                                else:
                                    msg_box(GameWindow, 'Please Enter a valid, Password. Use minimum one,Spcial Cherector/ Digit/,Capital letter & one Small letter')
                            else:
                                msg_box(GameWindow, 'Please enter valid OTP,or,Resend OTP')
                        else:
                            msg_box(GameWindow, 'Enter A Valid,Email address')
                        if Online_status and Verification and User_account_sheet.sheet_opend:
                            if status and row != -1 and col != -1:
                                re = User_account_sheet.update_cell(row, col+1, Password.text)
                                if re:
                                    msg_box(GameWindow, 'Your password is,Successfully changed.')
                                    status = False
                                    row = -1
                                    col = -1
                                    Email.text = ""
                                    Password.text = ''
                                    OTP.text = ''
                                    OTP.lenth = 0
                                    Email.lenth = 0
                                    Password.lenth = 0
                                    otp_sended = False
                                    otp_send_on = ''
                                    OTP_PASS = -1
                                    show_otp_caption = True
                                    show_email_caption = True
                                    show_password_caption = True
                                    return True
                                else:
                                    msg_box(GameWindow, 'Fail to reset your,Please try again or,check internet connection')
                            else:
                                msg_box(GameWindow, "Please check your,Email address or,Internet Connection")
                        elif Verification:
                            msg_box(GameWindow, "Please Check Your,Internet Connection.")
                    if collide(Mouse_x, Mouse_y, 547, 180, 614, 198) and validate_email(Email.text):
                        OTP_PASS = random.randint(100000, 999999)
                        if validate_email(Email.text):
                            if Online_status and User_account_sheet.sheet_opend:
                                caption('Please wait', Mouse_x, Mouse_y)
                                pygame.display.update()
                                status, row, col = email_already_reg(Email.text)
                                if status:
                                    if Gmail.login_status:
                                        send_mail = threading.Thread(target=send_otp,args=(Email.text, OTP_PASS, '', 1,))
                                        send_mail.start()
                                        otp_send_on = Email.text
                                        otp_sended = True
                                        msg_box(GameWindow, 'OTP Successfully sended,On your email,please check email.')
                                else:
                                    msg_box(GameWindow, 'Email are not,Registered')
                            else:
                                msg_box(GameWindow, "Unable to send OTP,please check your,Internet Connection!")
                        else:
                            msg_box(GameWindow, "Please enter a valid,Email address")

                    if view_pass_green.collide(Mouse_x, Mouse_y):
                        if show_password:
                            show_password = False
                        else:
                            show_password = True
                    if validate_password(Password.text,8):
                        Password.text_color = white
                    else:
                        Password.text_color = Red
                    if str(OTP_PASS) == OTP.text:
                        OTP.text_color = white
                    else:
                        OTP.text_color = Red
                    Email.get_tex_box_size_image_of_text()
                    OTP.get_tex_box_size_image_of_text()
                    if show_password:
                        Password.get_tex_box_size_image_of_text()
                    else:
                        Password.get_tex_box_size_image_of_password()

        GameWindow.blit(reset_img, [0,0])

        #----------------------------button and icons--------------------
        if show_email_caption and len(Email.text)==0:
            Email_caption.put_text()
        if show_password_caption and len(Password.text)==0:
            Password_caption.put_text()
        if show_otp_caption and len(OTP.text)==0:
            Otp_caption.put_text()

        if show_password:
            if view_pass_green.collide(Mouse_x, Mouse_y):
                view_pass_green.put()
            else:
                view_pass_white.put()
        else:
            if hide_pass_green.collide(Mouse_x, Mouse_y):
                hide_pass_green.put()
            else:
                hide_pass_white.put()

        if close_green.collide(Mouse_x, Mouse_y):
            close_green.put()
            caption('close',Mouse_x, Mouse_y)
        else:
            close_white.put()
        if Submit_green.collide(Mouse_x, Mouse_y):
            Submit_green.put()
        else:
            Submit_black.put()

        if collide(Mouse_x, Mouse_y, 244, 350, 477, 369):
            out_text_file(GameWindow, "Don't have an account? Sing up", 19, 244, 350, light_green, "Font/Gidole-Regular.otf")
        else:
            out_text_file(GameWindow, "Don't have an account? Sing up", 19, 244, 350, white, "Font/Gidole-Regular.otf")

        if otp_sended:
            if collide(Mouse_x, Mouse_y, 530, 180, 614, 198) and validate_email(Email.text):
                out_text_file(GameWindow, "Resend OTP", 19, 530, 180, light_green, "Font/Gidole-Regular.otf")
            elif validate_email(Email.text):
                out_text_file(GameWindow, "Resend OTP", 19, 530, 180, white, "Font/Gidole-Regular.otf")
        else:
            if collide(Mouse_x, Mouse_y, 547, 180, 614, 198) and validate_email(Email.text):
                out_text_file(GameWindow, "Send OTP", 19, 547, 180, light_green,"Font/Gidole-Regular.otf")
            elif validate_email(Email.text):
                out_text_file(GameWindow, "Send OTP", 19, 547, 180, white, "Font/Gidole-Regular.otf")
        #--------------------------getting input from user---------------
        if str(OTP_PASS) == OTP.text:
            OTP.text_color = white
        else:
            OTP.text_color = Red
        if validate_password(Password.text,8):
            Password.text_color = white
        else:
            Password.text_color = Red
        if Input_Email:
            Email.input_text(event_list)
        else:
            Email.put_text()
        if Input_Otp:
            OTP.input_numbers(event_list)
        else:
            OTP.put_text()

        if Input_Password:
            if show_password:
                Password.input_text(event_list)
            else:
                Password.input_password(event_list)
        else:
            Password.put_text()
        event_list = []

        if otp_sended:
            if not otp_send_on==Email.text:
                OTP.text_color = Red
                OTP.text = ''
                OTP.lenth = 0
                OTP.get_tex_box_size_image_of_text()
                OTP_PASS = -1
                otp_sended = False
        pygame.display.update()


def login():
    global Login_img
    global GameWindow
    global Mouse_y, Mouse_x
    global white
    global  light_green
    global Setting_obj
    global User_account_sheet
    global Login_img
    global create_ac_img
    Setting_obj.check_setting()
    login_black = Button(GameWindow, "Image/Login_black.png", 285, 296)
    login_green = Button(GameWindow, "Image/Login_green.png", 285, 296)
    close_white = Button(GameWindow, "Image/close_white.png", 17, 17)
    close_green = Button(GameWindow, "Image/close_green.png", 17, 17)
    view_pass_white = Button(GameWindow, "Image/view_pass_white.png", 568, 217)
    view_pass_green = Button(GameWindow, "Image/view_pass_green.png", 568, 217)
    hide_pass_white = Button(GameWindow, "Image/hide_pass_white.png", 568, 217)
    hide_pass_green = Button(GameWindow, "Image/hide_pass_green.png", 568, 217)
    Input_Email = False
    Input_Password = False
    Email = get_input(GameWindow, '', 163, 155, 20, 450, 390, white, white)
    Password = get_input(GameWindow, '', 163, 217, 20, 40, 390, white, white)
    Email.spcial_car = ['@', '.', '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '#', '$', '%', '&',
                        "'", '*', '+', '/', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';', '<',
                        '>', '[', '\\', ']']
    Password.spcial_car = ['@', '.', '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '#', '$', '%',
                           '&',
                           "'", '*', '+', '/', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';',
                           '<',
                           '>', '[', '\\', ']']
    event_list = []
    Email_caption = get_input(GameWindow, "Registered Email" , 163, 155, 20, 450, 390, white, white)
    Password_caption = get_input(GameWindow, 'Password', 163, 217, 20, 40, 390, white, white)
    Email_caption.get_tex_box_size_image_of_text()
    Password_caption.get_tex_box_size_image_of_text()
    show_password = False
    show_email_caption = True
    show_password_caption = True
    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                event_list.append(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if close_green.collide(Mouse_x, Mouse_y):
                        return
                    if collide(Mouse_x, Mouse_y, 74, 144, 620, 191):
                        show_email_caption = False
                        show_password_caption = True
                        Input_Email = True
                        Input_Password = False
                    if collide(Mouse_x, Mouse_y, 74, 208, 620, 252):
                        Input_Password = True
                        show_password_caption = False
                        show_email_caption = True
                        Input_Email  = False
                    if collide(Mouse_x, Mouse_y, 244, 346, 477, 365):
                        if Online_status and User_account_sheet.sheet_opend:
                            scroll_page_up_down(create_ac_img, 'down')
                            create_account()
                            scroll_page_up_down(Login_img, 'up')
                        else:
                            msg_box(GameWindow, "Please check your,internet connection.")
                    if collide(Mouse_x, Mouse_y, 286, 257, 619, 278) and validate_email(Email.text):
                        Reset_password(Email.text)
                    if login_green.collide(Mouse_x, Mouse_y):
                        if Online_status and User_account_sheet.sheet_opend:
                            caption('Please wait',Mouse_x, Mouse_y)
                            pygame.display.update()
                            status, data = check_email_and_password(Email.text, Password.text)
                            if status:
                                Setting_obj.Name, Setting_obj.Email, Setting_obj.Password, Setting_obj.PC_name, Setting_obj.Mac_Address, Setting_obj.IP_Address, Setting_obj.ISP, Setting_obj.Country, Setting_obj.State, Setting_obj.City, Setting_obj.DOCA = data
                                Setting_obj.login_status = True
                                Setting_obj.update_setting()
                                msg_box(GameWindow,"Successfully logged,in your account.")
                                return True
                                show_password = False
                                show_email_caption = True
                                show_password_caption = True
                                Email.text = ''
                                Email.lenth = 0
                                Password.text = ''
                                Password.lenth = 0
                            else:
                                msg_box(GameWindow, "Invalid,Email or Password")
                        else:
                            msg_box(GameWindow, "Please check your,internet connection.")
                    if view_pass_green.collide(Mouse_x, Mouse_y):
                        if show_password:
                            show_password = False
                        else:
                            show_password = True
                    Email.get_tex_box_size_image_of_text()
                    if show_password:
                        Password.get_tex_box_size_image_of_text()
                    else:
                        Password.get_tex_box_size_image_of_password()

        GameWindow.blit(Login_img, [0,0])

        #----------------------------button and icons--------------------
        if show_email_caption and len(Email.text)==0:
            Email_caption.put_text()
        if show_password_caption and len(Password.text)==0:
            Password_caption.put_text()

        if show_password:
            if view_pass_green.collide(Mouse_x, Mouse_y):
                view_pass_green.put()
            else:
                view_pass_white.put()
        else:
            if hide_pass_green.collide(Mouse_x, Mouse_y):
                hide_pass_green.put()
            else:
                hide_pass_white.put()

        if close_green.collide(Mouse_x, Mouse_y):
            close_green.put()
            caption('close',Mouse_x, Mouse_y)
        else:
            close_white.put()

        if login_green.collide(Mouse_x, Mouse_y):
            login_green.put()
        else:
            login_black.put()
        if collide(Mouse_x, Mouse_y, 244, 344, 477, 363):
            out_text_file(GameWindow, "Don't have an account? Sing up", 19, 244, 344, light_green, "Font/Gidole-Regular.otf")
        else:
            out_text_file(GameWindow, "Don't have an account? Sing up", 19, 244, 344, white, "Font/Gidole-Regular.otf")
        if collide(Mouse_x, Mouse_y, 286,257,619,278) and validate_email(Email.text):
            out_text_file(GameWindow, "Forget password?", 19, 486, 257, light_green,"Font/Gidole-Regular.otf")
        elif validate_email(Email.text):
            out_text_file(GameWindow, "Forget password?", 19, 486, 257, white, "Font/Gidole-Regular.otf")
        #--------------------------getting input from user---------------
        if Input_Email:
            Email.input_text(event_list)
        else:
            Email.put_text()
        if Input_Password:
            if show_password:
                Password.input_text(event_list)
            else:
                Password.input_password(event_list)
        else:
            Password.put_text()

        event_list = []
        pygame.display.update()


def create_account():
    global GameWindow
    global create_ac_img
    global GameWindow
    global Mouse_y, Mouse_x
    global MAC_ADDRESS
    global IP_ADDRESS
    global ONLINE_DATE
    global COMPUTER_NAME

    cancel_light_blue = Button(GameWindow,"Image/light_blue_button.png",329,338)
    cancel_dark_blue = Button(GameWindow, "Image/dark_blue_button.png", 330, 338)
    create_ac_light_orange = Button(GameWindow, "Image/light_orange_button.png", 473, 338)
    create_ac_dark_orange = Button(GameWindow, "Image/dark_orange_button.png", 473, 338)
    view_pass_green = Button(GameWindow, "Image/view_pass_green.png",595, 282)
    view_pass_white = Button(GameWindow, "Image/view_pass_white.png",595, 282)
    hide_pass_green = Button(GameWindow, "Image/hide_pass_green.png", 595, 282)
    hide_pass_white = Button(GameWindow, "Image/hide_pass_white.png", 595, 282)
    checked = Button(GameWindow, "Image/checked.png", 595, 95)
    warning = Button(GameWindow, "Image/warning_orange.png", 595, 95)
    checked2 = Button(GameWindow, "Image/checked.png", 595, 157)
    warning2 = Button(GameWindow, "Image/warning_orange.png", 595, 157)
    checked3 = Button(GameWindow, "Image/checked.png", 595, 218)
    warning3 = Button(GameWindow, "Image/warning_orange.png", 595, 218)
    checked4 = Button(GameWindow, "Image/checked.png", 561, 282)
    warning4 = Button(GameWindow, "Image/warning_orange.png", 561, 282)
    send_white = Button(GameWindow, "Image/send-button-white.png",561,218)
    send_green = Button(GameWindow, "Image/send-button-green.png",561,218)
    event_list = []
    Name = get_input(GameWindow, '',196, 94, 20,30,379,white,white)
    Email = get_input(GameWindow, '', 196, 156, 20, 350, 379, white, white)
    OTP = get_input(GameWindow, '', 196, 217, 20, 6, 379, white, white)
    Password = get_input(GameWindow, '', 196, 281, 20, 18, 379, white, white)
    Name.spcial_car = [' ']
    Email.spcial_car = ['@', '.', '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '#', '$', '%', '&',
                        "'", '*', '+', '/', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';', '<',
                        '>', '[', '\\', ']']
    Password.spcial_car = ['@', '.', '-', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '#', '$', '%', '&',
                        "'", '*', '+', '/', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';', '<',
                        '>', '[', '\\', ']']
    input_name = True
    input_email = False
    input_otp = False
    input_password = False
    Show_password = False
    icon_flag1 = True
    icon_flag2 = False
    icon_flag3 = False
    icon_flag4 = False
    verification_flag = False
    OTP_PASS = 0
    Otp_Send_button = False
    otp_send_on = ''
    otp_sended = False
    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                event_list.append(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if view_pass_green.collide(Mouse_x, Mouse_y):
                        if Show_password:
                            Password.get_tex_box_size_image_of_password()
                            Show_password = False
                        else:
                            Password.get_tex_box_size_image_of_password()
                            Show_password = True

                    if collide(Mouse_x, Mouse_y,196,89,575,124):
                        input_name = True
                        icon_flag1 = True
                        input_email = False
                        input_otp = False
                        input_password = False
                    if collide(Mouse_x, Mouse_y,196,151,575,186):
                        input_name = False
                        input_email = True
                        icon_flag2 = True
                        Otp_Send = False
                        input_otp = False
                        input_password = False
                    if collide(Mouse_x, Mouse_y,196,212,575,250):
                        input_name = False
                        input_email = False
                        input_otp = True
                        icon_flag3 = True
                        input_password = False
                    if collide(Mouse_x, Mouse_y,196,276,575,311):
                        input_name = False
                        input_email = False
                        input_otp = False
                        input_password = True
                        icon_flag4 = True
                    if Otp_Send_button and send_green.collide(Mouse_x, Mouse_y):
                        OTP_PASS = random.randint(100000, 999999)
                        if len(Name.text) >= 5:
                            if validate_email(Email.text):
                                if Online_status:
                                    if Gmail.login_status:
                                        send_mail = threading.Thread(target=send_otp,args=(Email.text, OTP_PASS, Name.text))
                                        send_mail.start()
                                        otp_send_on = Email.text
                                        otp_sended = True
                                        msg_box(GameWindow, 'OTP Successfully sended,On your email,please check email.')
                                    else:
                                        msg_box(GameWindow, "Unable to send OTP,please check your,Internet Connection!")
                                else:
                                    msg_box(GameWindow, "Unable to send OTP,please check your,Internet Connection!")
                            else:
                                msg_box(GameWindow, "Please enter a valid,Email address")
                                input_name = False
                                input_email = True
                                icon_flag2 = True
                                input_otp = False
                                input_password = False
                        else:
                            msg_box(GameWindow, 'Enter Minimum Five,charector in name')
                            input_name = True
                            input_email = False
                            icon_flag1 = True
                            input_otp = False
                            input_password = False

                    Name.get_tex_box_size_image_of_text()
                    Email.get_tex_box_size_image_of_text()
                    OTP.get_tex_box_size_image_of_text()
                    if Show_password:
                        Password.get_tex_box_size_image_of_text()
                    else:
                        Password.get_tex_box_size_image_of_password()
                    if cancel_light_blue.collide(Mouse_x, Mouse_y):
                        return
                    if create_ac_light_orange.collide(Mouse_x, Mouse_y):
                        if len(Name.text) >= 5:
                            if validate_email(Email.text):
                                if OTP.text == str(OTP_PASS):
                                    if validate_password(Password.text, 8):
                                        verification_flag = True
                                    else:
                                        msg_box(GameWindow,'Please Enter a valid, Password. Use minimum one,Spcial Cherector/ Digit/,Capital letter & one Small letter')
                                else:
                                    msg_box(GameWindow, 'Invalid OTP')
                            else:
                                msg_box(GameWindow, 'Please Enter Valid,Email Address')
                        else:
                            msg_box(GameWindow, 'Enter Minimum Five,charector in name')

                        if Online_status and verification_flag:
                            ip_address = ""
                            internet_service_provider = ""
                            city = ""
                            country = ""
                            State = ""
                            if User_account_sheet.sheet_opend:
                                caption('Creating Account', 478, 390)
                                pygame.display.update()
                                Reg_mail = Email.text.lower()
                                status, row, col = email_already_reg(Reg_mail)
                                if not status:
                                    if MAC_ADDRESS==None:
                                        MAC_ADDRESS = ''
                                    if COMPUTER_NAME==None:
                                        COMPUTER_NAME = ''
                                    if ONLINE_DATE ==None:
                                        ONLINE_DATE = ''
                                    if IP_ADDRESS!=None:
                                        try:
                                            ip_address = IP_ADDRESS['ip']
                                            internet_service_provider = IP_ADDRESS['org']
                                            city = IP_ADDRESS['city']
                                            country = IP_ADDRESS['country']
                                            State = IP_ADDRESS['region']
                                        except:
                                            ip_address = ""
                                            internet_service_provider = ""
                                            city = ""
                                            country = ""
                                            State = ""

                                    row = [Name.text,Reg_mail,Password.text,COMPUTER_NAME,MAC_ADDRESS,ip_address,internet_service_provider,country,State,city,ONLINE_DATE]
                                    #Name,Email,Password,PC Name,Mac Address,IP Address,ISP,Country,State,City,DOCA
                                    if Online_status and User_account_sheet.sheet_opend:
                                        re = User_account_sheet.insert_row_in_sheet(row,2)
                                    else:
                                        re = False
                                    if re:
                                        caption(' Account Created ', 478, 390)
                                        pygame.display.update()
                                        Name.text = ''
                                        Name.lenth = 0
                                        Email.text = ''
                                        Email.lenth = 0
                                        OTP.text = ''
                                        OTP.lenth = 0
                                        Password.text = ''
                                        Password.lenth = 0
                                        Name.get_tex_box_size_image_of_text()
                                        Email.get_tex_box_size_image_of_text()
                                        OTP.get_tex_box_size_image_of_text()
                                        Password.get_tex_box_size_image_of_password()
                                        input_name = False
                                        input_email = False
                                        input_otp = False
                                        input_password = False
                                        Show_password = False
                                        icon_flag1 = False
                                        icon_flag2 = False
                                        icon_flag3 = False
                                        icon_flag4 = False
                                        verification_flag = False
                                        OTP_PASS = 0
                                        Otp_Send_button = False
                                        otp_send_on = ''
                                        otp_sended = False
                                        msg_box(GameWindow, 'Account successfully,Created.')
                                        return True
                                    else:
                                        msg_box(GameWindow, 'Fail to create Account,Please try again.')
                                else:
                                    msg_box(GameWindow, "Email Address,already registered.")
                            else:
                                msg_box(GameWindow, 'Please Check Your,Internet Connection')
                        elif verification_flag:
                            msg_box(GameWindow, 'Please Check Your,Internet Connection')

        GameWindow.blit(create_ac_img, [0, 0])
        #---------- buttons and icons ----------------------
        if cancel_light_blue.collide(Mouse_x, Mouse_y):
            cancel_light_blue.put()
        else:
            cancel_dark_blue.put()
        if create_ac_light_orange.collide(Mouse_x, Mouse_y):
            create_ac_light_orange.put()
        else:
            create_ac_dark_orange.put()
        if Show_password:
            if view_pass_white.collide(Mouse_x, Mouse_y):
                view_pass_white.put()
            else:
                view_pass_green.put()
        else:
            if hide_pass_white.collide(Mouse_x, Mouse_y):
                hide_pass_white.put()
            else:
                hide_pass_green.put()
        if icon_flag1:
            if len(Name.text)>=5:
                checked.put()
            else:
                warning.put()
        if icon_flag2:
            if validate_email(Email.text):
                checked2.put()
            else:
                Otp_Send_button = False
                warning2.put()
        if icon_flag3:
            if validate_email(Email.text):
                Otp_Send_button = True
            if OTP.text == str(OTP_PASS):
                checked3.put()
            else:
                warning3.put()
        if icon_flag4:
            if validate_password(Password.text, 8):
                checked4.put()
            else:
                warning4.put()
        if otp_sended:
            if not otp_send_on == Email.text:
                OTP_PASS = 0
        if Otp_Send_button:
            if send_white.collide(Mouse_x, Mouse_y):
                send_white.put()
            else:
                send_green.put()
        #------------inputs---------------------
        if input_name:
            Name.input_text(event_list)
        else:
            Name.put_text()
        if input_email:
            Email.input_text(event_list)
        else:
            Email.put_text()
        if input_otp:
            OTP.input_numbers(event_list)
        else:
            OTP.put_text()
        if input_password:
            if Show_password:
                Password.input_text(event_list)
            else:
                Password.input_password(event_list)
        else:
            Password.put_text()
        event_list = []

        pygame.display.update()

def validate_password(password, minimum_lenth):
    spcial_car = ['@', '.', '-', '_', '!', '#', '$', '%', '&',
                  "'", '*', '+', '=', '?', '^', '`', '{', '|', '}', '~', '"', '(', ')', ',', ':', ';', '<',
                  '>', '[', ']']
    capital_char = False
    numbers = False
    small_char = False
    spcial_letters = False
    for e in password:
        if (e in spcial_car) and not spcial_letters:
            spcial_letters = True
        if (e >= 'a' and e <= 'z') and not small_char:
            small_char = True
        if (e >= 'A' and e <= 'Z') and not capital_char:
            capital_char = True
        if (e >= '0' and e <= '9') and not numbers:
            numbers = True
        if capital_char and numbers and small_char and spcial_letters:
            if len(password) >= minimum_lenth:
                return True
            break
    return False


def send_feedback():
    global Setting_obj
    Setting_obj = Setting_obj.check_setting()
    global Close_online_handler
    global Sheet
    global Mouse_y, Mouse_x
    global Online_status
    global IP_ADDRESS
    global COMPUTER_NAME
    global MAC_ADDRESS
    global ONLINE_DATE
    icon_flag_1 = False
    icon_flag_2 = False
    icon_flag_3 = False
    tick_icon = pygame.image.load("Image/tick.png")
    warning_icon = pygame.image.load("Image/warning.png")
    close_green = pygame.image.load("Image/close_green.png")
    close_white = pygame.image.load("Image/close_white.png")
    send_green = pygame.image.load("Image/send_green.png")
    send_white = pygame.image.load("Image/send_white.png")
    if Setting_obj.login_status and Setting_obj.online_score:
        Name = get_input(GameWindow, Setting_obj.Name, 190, 143, 20, 50, 395, white, white)
        Email = get_input(GameWindow, Setting_obj.Email, 190, 214, 20, 350, 395, white, white)
        Feedback = get_input(GameWindow, '', 190, 287, 20, 400, 395, white, white)
        Name.get_tex_box_size_image_of_text()
        Email.get_tex_box_size_image_of_text()
        name_flag = False
        email_flag = False
        feedback_flag = True
        icon_flag_1 = True
        icon_flag_2 = True
        icon_flag_3 = True
    else:
        Name = get_input(GameWindow, '', 190, 143, 20, 50, 395, white, white)
        Email = get_input(GameWindow, '', 190, 214, 20, 350, 395, white, white)
        Feedback = get_input(GameWindow, '', 190, 287, 20, 400, 395, white, white)
        name_flag = True
        email_flag = False
        feedback_flag = False
        icon_flag_1 = True
        icon_flag_2 = False
        icon_flag_3 = False

    Name.spcial_car = [' ']
    Email.spcial_car = ['@','.','-','_','1','2','3','4','5','6','7','8','9','0','!','#','$','%','&',"'",'*','+','/','=','?','^','`','{','|','}','~','"','(',')',',',':',';','<','>','[','\\',']']
    Feedback.spcial_car = [' ','@','.','-','_','1','2','3','4','5','6','7','8','9','0','!','#','$','%','&',"'",'*','+','/','=','?','^','`','{','|','}','~','"','(',')',',',':',';','<','>','[','\\',']']
    event_list = []
    pass_flag = False
    ip_address = ""
    internet_service_provider = ""
    city = ""
    country = ""
    State = ""

    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                event_list.append(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (Mouse_x >= 190 and Mouse_x <= 586) and (Mouse_y >= 136 and Mouse_y <= 175):
                        icon_flag_1 = True
                        name_flag = True
                        Email.get_tex_box_size_image_of_text()
                        Feedback.get_tex_box_size_image_of_text()
                        email_flag = False
                        feedback_flag = False
                    if (Mouse_x >= 190 and Mouse_x <= 586) and (Mouse_y >= 207 and Mouse_y <= 246):
                        icon_flag_2 = True
                        Name.get_tex_box_size_image_of_text()
                        Feedback.get_tex_box_size_image_of_text()
                        name_flag = False
                        email_flag = True
                        feedback_flag = False
                    if (Mouse_x >= 190 and Mouse_x <= 586) and (Mouse_y >= 280 and Mouse_y <= 320):
                        icon_flag_3 = True
                        name_flag = False
                        Name.get_tex_box_size_image_of_text()
                        Email.get_tex_box_size_image_of_text()
                        email_flag = False
                        feedback_flag = True
                    if (Mouse_x >= 17 and Mouse_x <= 48) and (Mouse_y >= 18 and Mouse_y <= 47):
                        return
                    if (Mouse_x >= 609 and Mouse_x <= 634) and (Mouse_y >= 342 and Mouse_y <= 365):
                        Email_msg = "Hi "+Name.text+",\n\nThank you very much for giving\nyour Feedback on Snake Game.\n\nShare, Support, Subscribe!!!\nYoutube: https://www.youtube.com/channel/UCCEBsUxSW7PyyCYLw8cyhvA\nTwitter:  https://twitter.com/brightgoal_in\nFacebook Page: https://www.facebook.com/brightgoal.in.Education\nFacebook Myself: https://www.facebook.com/harvindar.brightgoal\nInstagram: https://www.instagram.com/brightgoal.in/\nWebsite: https://www.brightgoal.in/\n\nPowered By : Harvindar Singh\nVisit on Store for More Product : https://www.instamojo.com/Brightgoal\n"
                        pass_flag = False
                        if icon_flag_1:
                            if len(Name.text)>=5:
                                if icon_flag_2:
                                    if validate_email(Email.text):
                                        if icon_flag_3:
                                            if len(Feedback.text)>=10:
                                                pass_flag = True
                                            else:
                                                msg_box(GameWindow, "Please Enter Minimum,10 Charector in Feedback")
                                        else:
                                            msg_box(GameWindow,"Please Enter Your,your feedback")
                                    else:
                                        msg_box(GameWindow,"Please Enter a Valid,Email Address")
                                else:
                                    msg_box(GameWindow,'Please Enter Your,Email Address')
                            else:
                                msg_box(GameWindow,"Please Enter Minimum,5 Charector in Name")
                        else:
                            msg_box(GameWindow,"Please Enter Your Name")
                        if Online_status and pass_flag:
                                if Feedback_sheet.sheet_opend:
                                    caption('Feedback Sending',604,364)
                                    pygame.display.update()
                                    if MAC_ADDRESS==None:
                                        MAC_ADDRESS = ''
                                    if COMPUTER_NAME==None:
                                        COMPUTER_NAME = ''
                                    if ONLINE_DATE ==None:
                                        ONLINE_DATE = ''
                                    if IP_ADDRESS!=None:
                                        try:
                                            ip_address = IP_ADDRESS['ip']
                                            internet_service_provider = IP_ADDRESS['org']
                                            city = IP_ADDRESS['city']
                                            country = IP_ADDRESS['country']
                                            State = IP_ADDRESS['region']
                                        except:
                                            ip_address = ""
                                            internet_service_provider = ""
                                            city = ""
                                            country = ""
                                            State = ""
                                    row = [Name.text,Email.text,Feedback.text,COMPUTER_NAME,ip_address,MAC_ADDRESS,internet_service_provider,country,State,city,ONLINE_DATE]
                                    re = Feedback_sheet.insert_row_in_sheet(row,2)
                                    if re:
                                        Setting_obj.feedback_sended = True
                                        Setting_obj.update_setting()
                                        caption(' Feedback Sended ', 604, 364)
                                        pygame.display.update()
                                        mail_send = threading.Thread(target=Gmail.send_mail,args=(Email.text,Email_msg,'Thanks For Your Feedback',))
                                        mail_send.start()
                                        msg_box(GameWindow,'Thanks For Your, FeedBack')
                                        Name.text = ""
                                        Name.lenth = 0
                                        Name.get_tex_box_size_image_of_text()
                                        Email.text = ""
                                        Email.lenth = 0
                                        Email.get_tex_box_size_image_of_text()
                                        Feedback.text = ""
                                        Feedback.lenth = 0
                                        Feedback.get_tex_box_size_image_of_text()
                                        icon_flag_1 = True
                                        icon_flag_2 = False
                                        icon_flag_3 = False
                                        name_flag = True
                                        email_flag = False
                                        feedback_flag = False
                                    else:
                                        msg_box(GameWindow,'Fail to send Feedback,Please Try Again!,or check,internet connection.')
                                else:
                                    msg_box(GameWindow,'Fail to send Feedback,Please Try Again!,or check,internet connection.')
                        elif pass_flag:
                            msg_box(GameWindow,"Please Check Your,Internet Connection?")


        GameWindow.blit(Send_feedback, [0, 0])
        if (Mouse_x >= 17 and Mouse_x <= 48) and (Mouse_y >= 18 and Mouse_y <= 47):
            GameWindow.blit(close_green, [17, 18])
        else:
            GameWindow.blit(close_white, [17, 18])
        if (Mouse_x >= 609 and Mouse_x <= 634) and (Mouse_y >= 342 and Mouse_y <= 365):
            GameWindow.blit(send_green, [609, 342])
        else:
            GameWindow.blit(send_white, [609, 342])
        if name_flag:
            Name.input_text(event_list)
        else:
            GameWindow.blit(Name.text_img, [192, 144])
        if email_flag:
            Email.input_text(event_list)
        else:
            GameWindow.blit(Email.text_img, [192, 215])
        if feedback_flag:
            Feedback.input_text(event_list)
        else:
            GameWindow.blit(Feedback.text_img, [192, 288])

        event_list = []
        if icon_flag_1 and len(Name.text) >= 5:
            GameWindow.blit(tick_icon, [599, 146])
        elif icon_flag_1:
            GameWindow.blit(warning_icon, [599, 146])
        if icon_flag_2 and validate_email(Email.text):
            GameWindow.blit(tick_icon, [599, 215])
        elif icon_flag_2:
            GameWindow.blit(warning_icon, [599, 215])
        if icon_flag_3 and len(Feedback.text) >= 10:
            GameWindow.blit(tick_icon, [599, 288])
        elif icon_flag_3:
            GameWindow.blit(warning_icon, [599, 288])
        pygame.display.update()
        clock.tick(32)


def setting():
    global Mouse_x,Mouse_y
    global Setting_obj
    global setting_img
    global Login_img
    global Online_status
    global User_account_sheet
    global GameWindow
    Setting_obj = Setting_obj.check_setting()

    button_img = pygame.image.load("Image/on_of_button.png")
    button_img_dark = pygame.image.load("Image/on_of_button_dark.png")
    more_product = pygame.image.load("Image/Product_store.png")
    more_product_border = pygame.image.load("Image/Product_store_border.png")
    facebook = pygame.image.load("Image/facebook.png")
    twitter = pygame.image.load("Image/twitter.png")
    brightgoal = pygame.image.load("Image/brightgoal.png")
    youtube = pygame.image.load("Image/youtube.png")
    youtube_grw = pygame.image.load("Image/youtube_grw.png")
    facebook_grw = pygame.image.load("Image/facebook_grw.png")
    brightgoal_grw = pygame.image.load("Image/brightgoal_grw.png")
    twitter_grw = pygame.image.load("Image/twitter_grw.png")

    Valume_dif = 0.0038314176245210726
    width, height, back_white = put_img(GameWindow, "Image/back_white_24.png", 20, 20, False)
    width, height, back_pink = put_img(GameWindow, "Image/back_pink_24.png", 20, 20, False)
    scroll_one_page_to_another(Menu_img, setting_img, "left")
    GameWindow.fill((35, 36, 54))
    if Setting_obj.online_score:
        radio_button_x = 527 #1. 483, 2. 527
    else:
        radio_button_x = 483
    radio_button_y = 212

    Sound_button_x = Setting_obj.Sound_button_x   #Starting_point -269, End_point - 483
    Sound_button_y = 105
    Music_button_x = Setting_obj.Music_Button_x   #Starting_point -269, End_point - 483
    Music_button_y = 155

    social_icon_x = 280
    social_icon_y = 348
    sound_flag = False
    music_flag = False

    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scroll_one_page_to_another(Menu_img, setting_img, "right")
                    return
            if (Mouse_x >= 13 and Mouse_x <= 13 + width) and (Mouse_y >= 355 and Mouse_y <= 355 + height):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    scroll_one_page_to_another(Menu_img, setting_img, "right")
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Mouse_x >= 483 and Mouse_x <= 550 and Mouse_y >= radio_button_y and Mouse_y <= radio_button_y + 24:
                    if radio_button_x == 483:
                        if Online_status:
                            scroll_page_up_down(Login_img, "down")
                            login()
                            scroll_page_up_down(setting_img, "up")
                            Setting_obj = Setting_obj.check_setting()
                            if not Setting_obj.login_status:
                                Setting_obj.online_score = False
                            else:
                                radio_button_x = 527
                                Setting_obj.online_score = True
                        else:
                            msg_box(GameWindow, "Please check your,Internet connection")
                    else:
                        radio_button_x = 483
                        Setting_obj.online_score = False
                        Setting_obj.login_status = False
                        Setting_obj.Name = ""
                        Setting_obj.Email = ""
                        Setting_obj.Password = ""
                        Setting_obj.PC_name = ""
                        Setting_obj.Mac_Address = ""
                        Setting_obj.IP_Address = ""
                        Setting_obj.ISP = ""
                        Setting_obj.Country = ""
                        Setting_obj.State = ""
                        Setting_obj.City = ""
                        Setting_obj.DOCA = ""
                    Setting_obj.update_setting()

                if Mouse_x >= Music_button_x and Mouse_x <= Music_button_x + 24 and Mouse_y > Music_button_y and Mouse_y < Music_button_y + 24:
                    music_flag = True
                if Mouse_x >= Sound_button_x and Mouse_x <= Sound_button_x + 24 and Mouse_y > Sound_button_y and Mouse_y < Sound_button_y + 24:
                    sound_flag = True
                if Mouse_x >= 300 and Mouse_x <= 300 + 120 and Mouse_y > 300 and Mouse_y < 300 + 29:
                    open_url("https://www.instamojo.com/Brightgoal/")
                if Mouse_x >= social_icon_x and Mouse_x <= social_icon_x + 24 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 19:
                    open_url("https://twitter.com/BrightGoal_in")
                if Mouse_x >= social_icon_x + 44 and Mouse_x <= social_icon_x + 44 + 20 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 20:
                    open_url("https://www.facebook.com/brightgoal.in.Education")
                if Mouse_x >= social_icon_x + 88 and Mouse_x <= social_icon_x + 88 + 26 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 19:
                    open_url("https://www.youtube.com/channel/UCCEBsUxSW7PyyCYLw8cyhvA?")
                if Mouse_x >= social_icon_x + 132 and Mouse_x <= social_icon_x + 132 + 23 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 23:
                    open_url("https://www.brightgoal.in/")
            if event.type == pygame.MOUSEBUTTONUP:
                music_flag = False
                sound_flag = False

        GameWindow.blit(setting_img, [0, 0])
        if Mouse_x >= 483 and Mouse_x <= 550 and Mouse_y >= radio_button_y and Mouse_y <= radio_button_y+24:
            GameWindow.blit(button_img_dark, [radio_button_x, radio_button_y])
        else:
            GameWindow.blit(button_img, [radio_button_x, radio_button_y])
        if radio_button_x == 483:
            custom_out_text(GameWindow, "OFF", 507, 549, 218, orange, 13)
        else:
            custom_out_text(GameWindow, "ON", 483, 529, 218, orange, 13)

        if music_flag:
            if Mouse_x -12 >= 268 and Mouse_x -12 <= 530:
                Music_button_x = Mouse_x - 12
                Setting_obj.Music_Valume = Valume_dif * (Music_button_x - 269)
            elif Mouse_x -12 < 268:
                Music_button_x = 269
                Setting_obj.Music_Valume = Valume_dif * (Music_button_x - 269)
            elif Mouse_x -12 > 530:
                Music_button_x = 530
                Setting_obj.Music_Valume = 1.0
            custom_out_text(GameWindow, str(int(0.3831417624521073*(Music_button_x-269))), 565, 590, 159, orange, 18)
            Setting_obj.Music_Button_x = Music_button_x
            Setting_obj.update_setting()
            Setting_obj.check_setting()
        if sound_flag:
            if Mouse_x - 12 >= 268 and Mouse_x - 12 <= 530:
                Sound_button_x = Mouse_x - 12
                Setting_obj.Sound_valume = Valume_dif * (Sound_button_x - 269)
            elif Mouse_x - 12 < 268:
                Sound_button_x = 269
                Setting_obj.Sound_valume = Valume_dif * (Sound_button_x - 269)
            elif Mouse_x - 12 > 530:
                Sound_button_x = 530
                Setting_obj.Sound_valume = 1.0
            custom_out_text(GameWindow, str(int(0.3831417624521073 * (Sound_button_x - 269))), 565, 590, 109, orange,18)
            Setting_obj.Sound_button_x = Sound_button_x
            Setting_obj.update_setting()
            Setting_obj.check_setting()



        if music_flag or Mouse_x >= Music_button_x and Mouse_x <= Music_button_x+24 and Mouse_y > Music_button_y and Mouse_y < Music_button_y+24:
            GameWindow.blit(button_img_dark, [Music_button_x, Music_button_y])
        else:
            GameWindow.blit(button_img, [Music_button_x, Music_button_y])

        pygame.draw.line(GameWindow,orange,[270, 117],[ Sound_button_x, 117],6)
        pygame.draw.line(GameWindow, orange, [270, 167], [Music_button_x, 167],6)

        if sound_flag or Mouse_x >= Sound_button_x and Mouse_x <= Sound_button_x + 24 and Mouse_y > Sound_button_y and Mouse_y < Sound_button_y + 24:
            GameWindow.blit(button_img_dark, [Sound_button_x, Sound_button_y])
        else:
            GameWindow.blit(button_img, [Sound_button_x, Sound_button_y])

        if Mouse_x >= 300 and Mouse_x <= 300+120 and Mouse_y > 300 and Mouse_y < 300+29:
            GameWindow.blit(more_product_border, [300, 300])
        else:
            GameWindow.blit(more_product, [300, 300])

        if Mouse_x >= social_icon_x and Mouse_x <= social_icon_x+24 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y+19:
            GameWindow.blit(twitter_grw, [social_icon_x-1, social_icon_y-1])
        else:
            GameWindow.blit(twitter, [social_icon_x, social_icon_y])  #276, 348
        if Mouse_x >= social_icon_x+44 and Mouse_x <= social_icon_x +44+ 20 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 20:
            GameWindow.blit(facebook_grw, [social_icon_x+43, social_icon_y-1])
        else:
            GameWindow.blit(facebook, [social_icon_x+44, social_icon_y])
        if Mouse_x >= social_icon_x+88 and Mouse_x <= social_icon_x +88+ 26 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 19:
            GameWindow.blit(youtube_grw, [social_icon_x+87, social_icon_y+1])
        else:
            GameWindow.blit(youtube, [social_icon_x+88, social_icon_y+2])
        if Mouse_x >= social_icon_x+132 and Mouse_x <= social_icon_x +132+ 23 and Mouse_y >= social_icon_y and Mouse_y <= social_icon_y + 23:
            GameWindow.blit(brightgoal_grw, [social_icon_x+131, social_icon_y-2])
        else:
            GameWindow.blit(brightgoal, [social_icon_x+132, social_icon_y-1])

        if (Mouse_x >= 13 and Mouse_x <= 13 + width) and (Mouse_y >= 355 and Mouse_y <= 355 + height):
            GameWindow.blit(back_white, [13, 355])
        else:
            GameWindow.blit(back_pink, [13, 355])
        pygame.display.update()

def about():
    global Mouse_y, Mouse_x
    global GameWindow
    global About_Img
    global Online_status
    global Feedback_sheet
    global Send_feedback
    global Game_Version
    global white
    scroll_one_page_to_another(Menu_img,About_Img,'left')
    Check_update_black = Button(GameWindow,'Image/Project_store_black.png',189,323)
    Send_feedback_black = Button(GameWindow, "Image/Send_feedback_black.PNG", 25, 323)
    Check_update_green = Button(GameWindow, 'Image/Project_store_green.png', 189, 323)
    Send_feedback_green = Button(GameWindow, "Image/Send_feedback_green.PNG", 25, 323)
    white_close = Button(GameWindow, "Image/close_white.png", 19,17)
    green_close = Button(GameWindow, "Image/close_green.png",19,17)

    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scroll_one_page_to_another(Menu_img, About_Img,'right')
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if green_close.collide(Mouse_x, Mouse_y):
                        scroll_one_page_to_another(Menu_img, About_Img, 'right')
                        return
                    if Check_update_green.collide(Mouse_x, Mouse_y):
                        open_url('https://www.instamojo.com/Brightgoal/')
                    if Send_feedback_green.collide(Mouse_x,Mouse_y):
                        if Online_status:
                            if Feedback_sheet.sheet_opend:
                                scroll_page_up_down(Send_feedback,"down")
                                send_feedback()
                                scroll_page_up_down(About_Img, "up")
                            else:
                                msg_box(GameWindow,"Please check your,Internet Connection!")
                        else:
                            msg_box(GameWindow, "Please check your,Internet Connection!")

        GameWindow.blit(About_Img, [0,0])
        out_text_file(GameWindow,"Version "+Game_Version, 18, 28, 283, white,"Font/Gidole-Regular.otf")
        if Send_feedback_green.collide(Mouse_x, Mouse_y):
            Send_feedback_green.put()
        else:
            Send_feedback_black.put()
        if Check_update_green.collide(Mouse_x, Mouse_y):
            Check_update_green.put()
        else:
            Check_update_black.put()
        if green_close.collide(Mouse_x, Mouse_y):
            caption('Close',Mouse_x,Mouse_y)
            green_close.put()
        else:
            white_close.put()
        pygame.display.update()


def play_game():
    global Mouse_x, Mouse_y
    global GameWindow
    global play_ground
    global Online_status
    global white
    global Setting_obj
    global Playing_Status
    global Local_high_score
    global Online_High_score_email
    global Online_High_score
    global Online_High_score_name
    global Online_score_sheet
    Setting_obj.check_setting()
    Snake_speed = 7
    online_score = online_score_record()
    record = score_record()
    snake_head_rl = pygame.image.load("Image/head_rl.png")
    snake_head_ud = pygame.image.load("Image/head_ud.png")
    snake_food = pygame.image.load("Image/food_apple.png")
    ex_food_pink = pygame.image.load("Image/ex_food_blue.png")
    ex_food_blue = pygame.image.load("Image/ex_food_pink.png")
    ex_low_food_img = pygame.image.load("Image/extra_low_food.png")
    ex_food_x = 0
    extra_food_value = 10
    ex_food_y = 0
    ex_food_count = 0
    Game_reset = 0
    flag = False
    ex_food_flag = False
    temp_head = snake_head_rl
    snake_body = pygame.image.load("Image/body.png")
    snake_lenth = 3
    Life = 3
    Score = 0
    snake_pos = [[94, 102], [107, 102], [120, 102]]
    food_x = 0
    food_y = 0
    food_x, food_y = get_food_pos(snake_pos, 0, 0)
    pro_bar = 0
    snake_x = 120
    snake_y = 102
    update_x = 13
    update_y = 0
    scroll_one_page_to_another(play_ground, Menu_img, "right")
    GameWindow.fill(light_blue)
    GameWindow.blit(play_ground, [0, 0])
    width, height, back_white = put_img(GameWindow, "Image/back_white_24.png", 13, 360, False)
    width, height, back_pink = put_img(GameWindow, "Image/back_pink_24.png", 13, 360, )
    pygame.display.update()
    high_score_name_old = ""
    high_score_email_old = ""
    high_score_old = 0
    ex_low_food_show = False
    ex_low_food_x = -20
    ex_low_food_y = -20
    ex_low_food_count = 0
    ex_low_pro_bar = 0
    ex_low_food_value = 0
    High_Score = record.get_High_score()
    Local_high_score = High_Score
    Playing_Status = True
    while True:
        for event in pygame.event.get():
            Mouse_x, Mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                Playing_Status = False
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scroll_one_page_to_another(play_ground, Menu_img, "left")
                    Playing_Status = False
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    pygame.image.save(GameWindow, 'temp1.png')
                    def_img = pygame.image.load('temp1.png')
                    define_pos(def_img,0,0)
                if event.key == pygame.K_LEFT and update_x!=13:
                    update_x = -13
                    temp_head = snake_head_rl
                    update_y = 0
                if event.key == pygame.K_RIGHT and update_x!=-13:
                    update_x = +13
                    temp_head = snake_head_rl
                    update_y = 0
                if event.key == pygame.K_UP and update_y!=13:
                    update_x = 0
                    temp_head = snake_head_ud
                    update_y = -13
                if event.key == pygame.K_DOWN and update_y!=-13:
                    update_x = 0
                    temp_head = snake_head_ud
                    update_y = +13
                if event.key == pygame.K_p:
                    temp = True
                    while temp:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    temp = False
                        Local_high_score = record.get_High_score()

            if (Mouse_x >= 13 and Mouse_x <= 13+width) and (Mouse_y >= 355 and Mouse_y <= 355+height):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    scroll_one_page_to_another(play_ground, Menu_img, "left")
                    Playing_Status = False
                    return

        GameWindow.blit(play_ground, [0, 0])
        if Online_status and Setting_obj.online_score and Setting_obj.login_status:
            high_score_name = Online_High_score_name
            high_score_email = Online_High_score_email
            high_score_online = Online_High_score
            if high_score_email != '' and high_score_name != '' and high_score_online!=0:
                high_score_email_old = high_score_email
                high_score_name_old = high_score_name
                high_score_old = high_score_online
                if high_score_email == Setting_obj.Email:
                    custom_out_text(GameWindow, "You are King of the Game", 192, 540, 10, white, 18, "Font/Gidole-Regular.otf")
                    if high_score_online < Score:
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(Score), 18, 22, 8,white, "Font/DroidSansMono.ttf")
                    else:
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(high_score_online), 18, 22, 8,white, "Font/DroidSansMono.ttf")
                else:
                    if high_score_online < Score:
                        custom_out_text(GameWindow, "You are King of the Game", 192, 540, 10, white, 18,"Font/Gidole-Regular.otf")
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(Score), 18, 22, 8, white,
                                      "Font/DroidSansMono.ttf")
                    else:
                        custom_out_text(GameWindow, "You v/s "+high_score_name, 192, 540, 10, white, 18, "Font/Gidole-Regular.otf")
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(high_score_online), 18, 22, 8, white,"Font/DroidSansMono.ttf")
            elif high_score_email_old != '' and high_score_name_old != '' and high_score_old != 0:
                if high_score_email_old == Setting_obj.Email:
                    custom_out_text(GameWindow, "You are King of the Game", 192, 540, 10, white, 18,
                                    "Font/Gidole-Regular.otf")
                    if high_score_old < Score:
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(Score), 18, 22, 8, white,
                                      "Font/DroidSansMono.ttf")
                    else:
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(high_score_old), 18, 22, 8,
                                      white, "Font/DroidSansMono.ttf")
                else:
                    if high_score_old < Score:
                        custom_out_text(GameWindow, "You are King of the Game", 192, 540, 10, white, 18,
                                        "Font/Gidole-Regular.otf")
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(Score), 18, 22, 8, white,
                                      "Font/DroidSansMono.ttf")
                    else:
                        custom_out_text(GameWindow, "You v/s " + high_score_name_old, 192, 540, 10, white, 18,
                                        "Font/Gidole-Regular.otf")
                        out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(high_score_old), 18, 22, 8,
                                      white, "Font/DroidSansMono.ttf")
            else:
                out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(High_Score), 18, 22, 8, white,"Font/DroidSansMono.ttf")
        else:
            out_text_file(GameWindow, "Score 0" + str(Score) + "/" + str(High_Score), 18, 22, 8, white,"Font/DroidSansMono.ttf")
        out_text_file(GameWindow, "Life 0"+str(Life), 18, 590, 8, white, "Font/DroidSansMono.ttf")
        if (Mouse_x >= 13 and Mouse_x <= 13 + width) and (Mouse_y >= 355 and Mouse_y <= 355 + height):
            GameWindow.blit(back_white, [13, 355])
        else:
            GameWindow.blit(back_pink, [13, 355])

        snake_y += update_y
        snake_x += update_x
        if ([snake_x, snake_y] in snake_pos) or (not ((snake_y >= 37 and snake_y <= 375) and (snake_x >= 3 and snake_x <= 679))):
            play_sound(Crash_sound,0,500)
            if Life == 0:
                stop_sound(Crash_sound)
                stop_sound(Eat_Food_sound)
                stop_sound(Show_extra_food_sound)
                scroll_page_up_down(game_over_img, "down")
                Playing_Status = False
                re = game_over(Score, High_Score)
                if re != 1:
                    scroll_one_page_to_another(game_over_img, Menu_img, "left")
                    Playing_Status = False
                    return
                Snake_speed = 7
                Playing_Status = True
                scroll_page_up_down(play_ground, "up")
                ex_food_x = 0
                extra_food_value = 10
                ex_food_y = 0
                ex_food_count = 0
                ex_low_food_count = 0
                ex_low_food_y = -20
                ex_low_food_x = -20
                ex_low_food_show = False
                ex_low_pro_bar = False
                ex_low_food_value = 10
                Game_reset = 0
                flag = False
                ex_food_flag = False
                temp_head = snake_head_rl
                snake_lenth = 3
                Life = 3
                Score = 0
                snake_pos = [[94, 102], [107, 102], [120, 102]]
                food_x, food_y = get_food_pos(snake_pos, 0, 0)
                pro_bar = 0
                snake_x = 120
                snake_y = 102
                update_x = 13
                update_y = 0
                continue
            else:
                Game_reset = len(snake_pos)-3
                snake_lenth = 3
                snake_pos = [[94, 102], [107, 102], [120, 102]]
                Life -= 1
                snake_x = 120
                snake_y = 102
                update_x = 13
                update_y = 0
                continue

        temp = snake_lenth
        while temp!=0:
            temp -= 1
            if temp+1 == snake_lenth:
                GameWindow.blit(temp_head, snake_pos[temp])
            else:
                GameWindow.blit(snake_body, snake_pos[temp])

        snake_pos.append([snake_x, snake_y])

        if Game_reset!=0:
            snake_lenth += 1
            if snake_y == food_y and snake_x == food_x:
                play_sound(Eat_Food_sound)
                Score += 1
                ex_food_count += 1
                ex_low_food_count +=1
                food_x, food_y = get_food_pos(snake_pos, food_x, food_y)
                High_Score = record.update_score(Score)
            elif (ex_food_y == snake_y and ex_food_x == snake_x) or (ex_food_y + 4 == snake_y and ex_food_x == snake_x) or (ex_food_y == snake_y and ex_food_x + 4 == snake_x) or (ex_food_y + 4 == snake_y + 4 and ex_food_x + 4 == snake_x):
                play_sound(Eat_Food_sound)
                Score += int(extra_food_value)
                if Snake_speed<12:
                    Snake_speed  += 1
                ex_food_x = 0
                ex_food_y = 0
                High_Score = record.update_score(Score)
                pro_bar = 0
                ex_food_flag = False
                flag = False
            elif (ex_low_food_y == snake_y and ex_low_food_x == snake_x) or (ex_low_food_y + 4 == snake_y and ex_low_food_x == snake_x) or (ex_low_food_y == snake_y and ex_low_food_x + 4 == snake_x) or (ex_low_food_y + 4 == snake_y + 4 and ex_low_food_x + 4 == snake_x):
                play_sound(Eat_Food_sound)
                ex_low_food_y = -20
                ex_low_food_x = -20
                Score += int(ex_low_food_value)
                if Snake_speed > 6:
                    Snake_speed -= 1
                High_Score = record.update_score(Score)
                ex_low_pro_bar = 0
                ex_low_food_show = False
            Game_reset -= 1
        else:
            if snake_y == food_y and snake_x == food_x:
                play_sound(Eat_Food_sound)
                snake_lenth += 1
                Score+=1
                ex_food_count += 1
                ex_low_food_count += 1
                food_x, food_y = get_food_pos(snake_pos, food_x, food_y)
                High_Score = record.update_score(Score)
            elif (ex_food_y == snake_y and ex_food_x == snake_x) or (ex_food_y+4 == snake_y and ex_food_x == snake_x) or (ex_food_y == snake_y and ex_food_x+4 == snake_x) or (ex_food_y+4 == snake_y+4 and ex_food_x+4 == snake_x):
                play_sound(Eat_Food_sound)
                snake_lenth += 1
                ex_food_x = 0
                ex_food_y = 0
                Score += int(extra_food_value)
                if Snake_speed<12:
                    Snake_speed  += 1
                High_Score = record.update_score(Score)
                pro_bar = 0
                ex_food_flag = False
                flag = False
            elif (ex_low_food_y == snake_y and ex_low_food_x == snake_x) or (ex_low_food_y + 4 == snake_y and ex_low_food_x == snake_x) or (ex_low_food_y == snake_y and ex_low_food_x + 4 == snake_x) or (ex_low_food_y + 4 == snake_y + 4 and ex_low_food_x + 4 == snake_x):
                play_sound(Eat_Food_sound)
                snake_lenth += 1
                ex_low_food_y = -20
                ex_low_food_x = -20
                Score += int(ex_low_food_value)
                if Snake_speed > 6:
                    Snake_speed -= 1
                High_Score = record.update_score(Score)
                ex_low_pro_bar = 0
                ex_low_food_show = False
            else:
                snake_pos = snake_pos[1::]
        Local_high_score = High_Score
        if ex_low_food_count == 25:
            ex_low_food_show = True
            play_sound(Show_extra_food_sound)
            ex_low_food_x, ex_low_food_y = get_extra_food_pos(snake_pos, food_x, food_y)
            ex_low_food_count = 0
            ex_low_pro_bar = 692
            ex_low_food_value = 10

        if ex_low_pro_bar > 0:
            pygame.draw.line(GameWindow, light_green,[0, 35], [ex_low_pro_bar, 35], 3)
            ex_low_pro_bar -= 18
            ex_low_food_value -= 0.2601456816
        else:
            ex_low_food_show = False
            ex_low_food_y  = -20
            ex_low_food_x = -20

        if ex_low_food_show:
            GameWindow.blit(ex_low_food_img, [ex_low_food_x, ex_low_food_y])

        if ex_food_count == 10:
            ex_food_flag = True
            play_sound(Show_extra_food_sound)
            ex_food_x, ex_food_y = get_extra_food_pos(snake_pos, food_x, food_y)
            ex_food_count = 0
            extra_food_value = 10
            pro_bar = 692
        if pro_bar > 0:
            pygame.draw.line(GameWindow, Light_Pink,[0, 35], [pro_bar, 35], 3)
            pro_bar -= 18
            extra_food_value -= 0.2601456816
        else:
            ex_food_flag = False
            flag = False
            ex_food_x = 0
            ex_food_y = 0

        if ex_food_flag:
            if flag:
                GameWindow.blit(ex_food_pink, [ex_food_x, ex_food_y])
                flag = False
            else:
                GameWindow.blit(ex_food_blue, [ex_food_x, ex_food_y])
                flag = True

        GameWindow.blit(snake_food, [food_x, food_y])
        pygame.display.update()
        clock.tick(Snake_speed)


def game_over(score, game_high_score=0):
    global Online_status
    global Feedback_sheet
    global Setting_obj
    global Feedback_sending
    global light_green
    global white
    global GameWindow
    Show_Online_score = False
    you_are_king = False
    Setting_obj = Setting_obj.check_setting()
    if Online_status:
        if Setting_obj.login_status and Setting_obj.online_score:
            Show_Online_score = True
            Online_score = online_score_record()
            High_score = Online_score.get_High_score()
            High_score_email = Online_score.get_High_score_email()
            if High_score_email == Setting_obj.Email:
                you_are_king = True
            High_score_name = Online_score.get_High_score_name()
            if score > High_score:
                Online_score.update_score(Setting_obj.Name, score, Setting_obj.Email)
                you_are_king = True
                High_score_email = Setting_obj.Email
                High_score_name = Setting_obj.Name
                High_score = score
        else:
            Show_Online_score = False
            you_are_king = False
            Record  = score_record()
            High_score = game_high_score
    else:
        Show_Online_score = False
        you_are_king = False
        Record = score_record()
        High_score = game_high_score

    if score !=0 and High_score!=0:
        temp = High_score/5
        star_value = score/temp
    else:
        star_value = 0
    temp = 0
    temp_2 = 0
    high_temp = 0
    star_x = 344
    star_y = 166
    diffrence = 26
    king_img = pygame.image.load("Image/king.png")
    home_green = Button(GameWindow,"Image/home_green.png", 133, 20)
    home_white = Button(GameWindow, "Image/home_white.png", 133, 20)
    replay_green = Button(GameWindow, "Image/replay_green.png", 178, 20)
    replay_white = Button(GameWindow, "Image/replay_white.png", 178, 20)
    star = pygame.image.load("Image/star.png")
    star_blank = pygame.image.load("Image/star_blank.png")
    GameWindow.blit(game_over_img, [0, 0])
    GameWindow.blit(star_blank, [star_x, star_y])
    GameWindow.blit(star_blank, [star_x + diffrence, star_y])
    GameWindow.blit(star_blank, [star_x + (diffrence * 2), star_y])
    GameWindow.blit(star_blank, [star_x + (diffrence * 3), star_y])
    GameWindow.blit(star_blank, [star_x + (diffrence * 4), star_y])
    pygame.display.update()
    clock.tick(1)

    while True:
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_green.collide(Mouse_x, Mouse_y):
                    return 0
                if replay_green.collide(Mouse_x, Mouse_y):
                    return 1


        GameWindow.blit(game_over_img, [0, 0])
        GameWindow.blit(star_blank, [star_x, star_y])
        GameWindow.blit(star_blank, [star_x+diffrence, star_y])
        GameWindow.blit(star_blank, [star_x+(diffrence*2), star_y])
        GameWindow.blit(star_blank, [star_x+(diffrence*3), star_y])
        GameWindow.blit(star_blank, [star_x+(diffrence*4), star_y])

        if star_value>=1 and temp >= 1:
            GameWindow.blit(star, [star_x, star_y])
        if star_value >= 2 and temp >= 2:
            GameWindow.blit(star, [star_x + diffrence, star_y])
        if star_value >= 3 and temp >= 3:
            GameWindow.blit(star, [star_x + (diffrence * 2), star_y])
        if star_value >= 4 and temp >= 4:
            GameWindow.blit(star, [star_x + (diffrence * 3), star_y])
        if star_value >= 5 and temp >= 5:
            GameWindow.blit(star, [star_x + (diffrence * 4), star_y])
        if temp <= 5:
            temp+=0.1

        if home_green.collide(Mouse_x, Mouse_y):
            home_green.put()
            caption("Back To Home", Mouse_x, Mouse_y)
        else:
            home_white.put()

        if replay_green.collide(Mouse_x, Mouse_y):
            replay_green.put()
            caption("Replay", Mouse_x, Mouse_y)
        else:
            replay_white.put()

        if Show_Online_score:
            if you_are_king:
                GameWindow.blit(king_img, [384, 17])
                custom_out_text(GameWindow, "Your Highest Score", 462, 611, 289, white, 20, "Font/Gidole-Regular.otf")
                custom_out_text(GameWindow, High_score_name, 230, 578, 62, white, 18, "Font/Gidole-Regular.otf")
                custom_out_text(GameWindow, "You are the king of this game because you made the", 230, 578, 79, white, 18,"Font/Gidole-Regular.otf")
                custom_out_text(GameWindow, "highest score in the community of this game.", 230, 578, 96, white, 18,"Font/Gidole-Regular.otf")
            else:
                custom_out_text(GameWindow, High_score_name, 462, 611, 289, white, 20, "Font/Gidole-Regular.otf")
                custom_out_text(GameWindow, "You v/s "+High_score_name, 230, 578, 62, white, 22, "Font/Gidole-Regular.otf")
            custom_out_text(GameWindow, 'Your Score', 209, 340, 289, white, 20, "Font/Gidole-Regular.otf")
            custom_out_text(GameWindow, str(temp_2), 209, 340, 320, light_green, 22)
            custom_out_text(GameWindow, str(high_temp), 462, 611, 320, light_green, 22)
        else:
            custom_out_text(GameWindow, str(temp_2), 209, 340, 289, light_green, 22)
            custom_out_text(GameWindow, str(high_temp), 462, 611, 289, light_green, 22)
        pygame.display.update()
        if temp_2<score:
            temp_2+=5
        else:
            temp_2 = score
        if high_temp<High_score:
            high_temp += 5
        else:
            high_temp = High_score
            if Online_status and Feedback_sending:
                if Feedback_sheet.sheet_opend:
                    if not Setting_obj.feedback_sended:
                        scroll_page_up_down(Send_feedback,'down')
                        send_feedback()
                        Feedback_sending = False
                        scroll_page_up_down(game_over_img,'up')
        clock.tick(100)

def get_extra_food_pos(snake_pos, old_x, old_y):
    while True:
        x = (random.randint(2, 51)*13)+3
        while True:
            y = (random.randint(2, 25)*13)+37
            if x < 42 and y > 336:
                continue
            break
        if [x, y] in snake_pos or (y == old_y and x == old_x):
            continue
        return x, y

def get_food_pos(snake_pos, old_x, old_y):
    while True:
        x = (random.randint(1, 52)*13)+3
        while True:
            y = (random.randint(1, 26)*13)+37
            if x < 42 and y > 336:
                continue
            break
        if [x, y] in snake_pos or (y == old_y and x == old_x):
            continue
        return x, y

def scroll_one_page_to_another(page_1, page_2,direction):
    global GameWindow
    play_sound(Slide_sound)
    width = page_1.get_width()
    if direction=="left":
        x1=width
        while x1>=0:
            #GameWindow.blit(page_1, [x, 0])
            GameWindow.blit(page_2, [x1,0])
            #x-=26
            x1-=20
            pygame.display.update()
    if direction=="right":
        x1 = -width
        while x1 <= 0:
            GameWindow.blit(page_1, [x1, 0])
            #GameWindow.blit(page_2, [x, 0])
            #x += 1
            x1 += 20
            pygame.display.update()

def scroll_page_up_down(page, direction):
    global GameWindow
    play_sound(Slide_sound)
    height = page.get_height()
    if direction == "up":
        y = height
        while y > 0:
            GameWindow.blit(page, [0, y])
            y -= 12
            pygame.display.update()
    if direction == "down":
        y = -height
        while y <= 0:
            GameWindow.blit(page, [0, y])
            pygame.display.update()
            y += 12

def close_game():
    global controling_thread
    controling_thread = False
    pygame.quit()
    sys.exit()

def out_text(text, size, x, y, color, font_style=None, bk_color=None):
    global GameWindow
    font = pygame.font.SysFont(font_style, size)
    text_img = font.render(text, True, color, bk_color)
    GameWindow.blit(text_img, [x, y])

def out_text_file(surface, text, size, x, y, color, font_file, return_img = False, bk_color=None):
    try:
        font = pygame.font.Font(font_file, size)
    except OSError:
        font = pygame.font.SysFont(None, size)
    text_img = font.render(text, True, color, bk_color)
    if return_img:
        return text_img
    surface.blit(text_img, [x, y])