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