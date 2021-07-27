import requests
import discord
import json

url = 'https://discord.com/api/webhooks/869466927699984394/SoFj8iaKBbzH_uA-GYV5aNwn0iK-jVcb6CS1tiG6PCIEkHjtI8VMJqj-KLCVW9TxFMsm'

while True:
    message = input()
    r= requests.post(url, data={"content": message, "username": "wewewew", "avatar_url": "https://i.imgur.com/oBPXx0D.png"})