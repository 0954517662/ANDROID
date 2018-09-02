# YUKIESTREETBOT
# KHIE WAS HERE
from Lineoat.linepy import *
from Lineoat.akad.ttypes import Message
from Lineoat.akad.ttypes import ContentType as Type
from Lineoat.akad.ttypes import ChatRoomAnnouncementContents
from Lineoat.akad.ttypes import ChatRoomAnnouncement
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, ffmpy, wikipedia, atexit, datetime, pafy, youtube_dl
_session = requests.session()
from gtts import gTTS
from googletrans import Translator
#==============================================================================================================
botStart = time.time()
#==============================================================================================================
client = LINE ()
#==============================================================================================================
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
stickersOpen = codecs.open("sticker.json","r","utf-8")
imagesOpen = codecs.open("image.json","r","utf-8")
#==============================================================================================================
mid = client.getProfile().mid
#==============================
clientMID = client.profile.mid
#==============================
clientProfile = client.getProfile()
#==============================================================================================================
clientSettings = client.getSettings()
#==============================================================================================================
clientPoll = OEPoll(client)
#==============================================================================================================
admin = "ue4117356009586eb55366d1199e56589"
owner = "ue4117356009586eb55366d1199e56589"
Bots=[mid,"ue4117356009586eb55366d1199e56589"]
#==============================================================================================================
#==============================================================================================================
contact = client.getProfile()
backup = client.getProfile()
backup.displayName = contact.displayName
backup.statusMessage = contact.statusMessage
backup.pictureStatus = contact.pictureStatus
squareChatMid='ue4117356009586eb55366d1199e56589'
#helpMute = """Switched to normal mode"""
#helpUnmute = """I'll be here when you need me"""
#==============================================================================================================
msg_dict = {}
msg_image={}
msg_video={}
msg_sticker={}
unsendchat = {}
temp_flood = {}
wbanlist = []

read = {
    "readPoint":{},
    "readMember":{},
    "readTime":{},
    "ROM":{},
}
sider = {
  "point":{},
  "cyduk":{},
  "sidermem":{}
}
#==============================================================================================================
myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}
#==============================================================================================================
myProfile["displayName"] = clientProfile.displayName
myProfile["statusMessage"] = clientProfile.statusMessage
myProfile["pictureStatus"] = clientProfile.pictureStatus
#==============================================================================================================
read = json.load(readOpen)
settings = json.load(settingsOpen)
images = json.load(imagesOpen)
stickers = json.load(stickersOpen)
msg_dict = {}
bl = ["ue4117356009586eb55366d1199e56589"]

try:
    with open("Log_data.json","r",encoding="utf_8_sig") as f:
        msg_dict = json.load(f.read())
except:
    print("Couldn't read Log data")
#        with open('welcomemsg.json', 'r') as fp:
#          welcomemsg = json.load(fp)     
#==============================================================================================================
#if settings["restartPoint"] != None:
#    client.sendMessage(settings["restartPoint"], "Programs return!")
#    settings["restartBot"] = None
#==============================================================================================================
def RhyN_(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@Rh'
        client.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
#==============================================================================================================
                        
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')

def delExpire():
    if temp_flood != {}:
        for tmp in temp_flood:
            if temp_flood[tmp]["expire"] == True:
                if time.time() - temp_flood[tmp]["time"] >= 3*10:
                    temp_flood[tmp]["expire"] = False
                    temp_flood[tmp]["time"] = time.time()
                    try:
                        userid = "https://line.me/ti/p/~" + client.profile.userid
                        client.sendFooter(tmp, "Spam is over , Now Bots Actived !", str(userid), "http://dl.profile.line-cdn.net/"+client.getContact(clientMID).pictureStatus, client.getContact(clientMID).displayName)
                    except Exception as error:
                        logError(error)

def load():
    global images
    global stickers
    with open("image.json","r") as fp:
        images = json.load(fp)
    with open("sticker.json","r") as fp:
        stickers = json.load(fp)
        
def sendSticker(to, version, packageId, stickerId):
    contentMetadata = {
        'STKVER': version,
        'STKPKGID': packageId,
        'STKID': stickerId
    }
    client.sendMessage(to, '', contentMetadata, 7)

def sendImage(to, path, name="image"):
    try:
        if settings["server"] == "VPS":
            client.sendImageWithURL(to, str(path))
    except Exception as error:
        logError(error)
#==============================================================================================================
def logError(text):
    client.log("[ INFO ] ERROR : " + str(text))
    time_ = datetime.datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time_), text))
#==============================================================================================================
def delete_log():
    ndt = datetime.datetime.now()
    for data in msg_dict:
        if (datetime.datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > datetime.timedelta(1):
            del msg_dict[msg_id]
            
def changeVideoAndPictureProfile(pict, vids):
    try:
        files = {'file': open(vids, 'rb')}
        obs_params = client.genOBSParams({'oid': clientMID, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return "Failed update profile"
        client.updateProfilePicture(pict, 'vp')
        return "Success update profile"
    except Exception as e:
        raise Exception("Error change video and picture profile {}".format(str(e)))

def changeProfileVideo(to):
    if settings['changeProfileVideo']['picture'] == None:
        return client.sendMessage(to, "Foto tidak ditemukan")
    elif settings['changeProfileVideo']['video'] == None:
        return client.sendMessage(to, "Video tidak ditemukan")
    else:
        path = settings['changeProfileVideo']['video']
        files = {'file': open(path, 'rb')}
        obs_params = client.genOBSParams({'oid': client.getProfile().mid, 'ver': '2.0', 'type': 'video', 'cat': 'vp.mp4'})
        data = {'params': obs_params}
        r_vp = client.server.postContent('{}/talk/vp/upload.nhn'.format(str(client.server.LINE_OBS_DOMAIN)), data=data, files=files)
        if r_vp.status_code != 201:
            return client.sendMessage(to, "Gagal update profile")
        path_p = settings['changeProfileVideo']['picture']
        settings['changeProfileVideo']['status'] = False
        client.updateProfilePicture(path_p, 'vp')
        
def speedtest(à¸§à¸´à¸à¸²à¸à¸µ):
    à¸à¸²à¸à¸µ, à¸§à¸´à¸à¸²à¸à¸µ = divmod(à¸§à¸´à¸à¸²à¸à¸µ,60)
    à¸à¸±à¹à¸§à¹à¸¡à¸, à¸à¸²à¸à¸µ = divmod(à¸à¸²à¸à¸µ,60)
    à¸§à¸±à¸, à¸à¸±à¹à¸§à¹à¸¡à¸ = divmod(à¸à¸±à¹à¸§à¹à¸¡à¸,24)
    à¸­à¸²à¸à¸´à¸à¸¢à¹, à¸§à¸±à¸ = divmod(à¸§à¸±à¸,7)
    if à¸§à¸±à¸ == 0:
        return '%02d' % (à¸§à¸´à¸à¸²à¸à¸µ)
    elif à¸§à¸±à¸ > 0 and à¸­à¸²à¸à¸´à¸à¸¢à¹ == 0:
        return '%02d' %(à¸§à¸´à¸à¸²à¸à¸µ)
    elif à¸§à¸±à¸ > 0 and à¸­à¸²à¸à¸´à¸à¸¢à¹ > 0:
        return '%02d' %(à¸§à¸´à¸à¸²à¸à¸µ)
#==============================================================================================================
def command(text):
    pesan = text.lower()
    if pesan.startswith(settings["keyCommand"]):
        cmd = pesan.replace(settings["keyCommand"],"")
    else:
        cmd = "Undefined command"
    return cmd
#==============================================================================================================
helpmsg ="""
â âââââââââââââââââââââ
â Me
â .à¸à¸
â à¹à¸­à¸à¸µà¹à¸£à¸²
â à¸à¸´à¹à¸à¹à¸£à¸²
â à¸­à¸±à¸à¸à¸·à¹à¸­ ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸­à¸±à¸à¸à¸±à¸ª ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸­à¸±à¸à¸£à¸¹à¸
â à¸à¸·à¹à¸­à¹à¸£à¸²
â à¸à¸´à¸ªà¹à¸£à¸²
â à¸à¸±à¸ªà¹à¸£à¸²
â à¸§à¸µà¸à¸µà¹à¸­à¹à¸£à¸²
â à¸à¸à¹à¸£à¸²
â à¹à¸­à¸à¸µã@ã
â à¸à¸ã@ã
â à¸à¸·à¹à¸­ã@ã
â à¸à¸±à¸ªã@ã
â à¸à¸´à¸ªã@ã
â à¸§à¸µà¸à¸µà¹à¸­ã@ã
â à¸à¸ã@ã
â à¸à¸¶à¸à¸«à¸¡à¸ã@ã
â à¸à¸¶à¸à¸«à¸¡à¸ãà¹à¸à¸ à¸ªà¸ã
â à¹à¸­à¸à¸µà¹à¸¥à¸à¹ãid à¹à¸¥à¸à¹ã
â à¸à¸­à¸£à¸¹à¸ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¹à¸à¸µà¸¢à¸ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸¥à¹à¸²à¸à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¹à¸à¸à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡
â à¸à¸²à¸à¸¹à¸ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸¢à¸¹à¸à¸¹à¸
â à¸à¸£à¸°à¸à¸²à¸¨: ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸¹à¸ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸¹à¸à¸à¸¸à¸à¸«à¹à¸­à¸ ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¹à¸²à¸§
â à¸¥à¸à¹à¸à¸
â à¹à¸à¸¥à¸° ãà¸­à¸­à¸à¸«à¹à¸­à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ã
â à¹à¸à¸à¸£à¸­à¸à¸«à¸à¸±à¸
â à¸à¸à¹à¸à¸à¸¥à¸¸à¹à¸¡
â à¸à¸à¸ªà¸£à¹à¸²à¸à¸à¸¥à¸¸à¹à¸¡
â à¸à¸²à¸¡ ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸ªà¸§à¸±à¸ªà¸à¸µãà¸à¸·à¹à¸­ã
â Fcãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸­à¸­à¸
â à¹à¸à¸
â à¸¡à¸­à¸
â à¸à¹à¸­à¸¡à¸¹à¸¥
â à¹à¸à¸´à¹à¸¡à¹à¸à¸·à¹à¸­à¸ã@ã
â à¸¥à¸à¹à¸à¸·à¹à¸­à¸ã@ã
â à¸¥à¹à¸²à¸à¹à¸à¸·à¹à¸­à¸à¸à¸±à¹à¸à¸«à¸¡à¸
â à¸¢à¸à¹à¸¥à¸´à¸ãà¸à¸³à¸à¸§à¸ã
â à¸£à¸¹à¸à¸«à¹à¸­à¸
â à¸­à¸±à¸à¸£à¸¹à¸à¸à¸¥à¸¸à¹à¸¡
â à¸à¹à¸²à¸
â à¸à¹à¸­à¸¡à¸¹à¸¥à¸à¸¥à¸¸à¹à¸¡
â à¸à¸à¹à¸à¸à¸¥à¸¸à¹à¸¡
â à¹à¸à¸·à¹à¸­à¸
â à¸à¸¥à¹à¸­à¸ã@ã
â à¸à¸¥à¹à¸­à¸
â à¹à¸§à¸¥à¸²
â à¸à¸³ãà¸ªà¹à¸à¸à¸à¸à¸à¸à¸µà¹à¸à¸°à¸¢à¸±à¸à¸à¸³à¸¥à¸ã
â à¸à¸¥à¸à¸à¸³ãà¸ªà¹à¸à¸à¸à¸à¸à¸à¸µà¹à¸à¸°à¸¥à¹à¸²à¸à¸à¸³à¸¥à¸ã
â à¸à¸à¸à¸³
â à¸¥à¹à¸²à¸à¸à¸³
â à¹à¸à¸à¸à¸³
â à¹à¸à¸´à¸à¸¥à¸´à¹à¸
â à¸à¸´à¸à¸¥à¸´à¹à¸
â Spam on|num|text
â à¸à¸±à¹à¸à¸à¸·à¹à¸­à¸à¸¥à¸¸à¹à¸¡ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸£à¸±à¸à¸à¸¥à¸­ãà¸à¸³à¸à¸§à¸ã à¸£à¸±à¸à¹à¸à¸£
â à¸§à¹à¸²ãà¸à¸³à¸à¸§à¸ @ãà¸ªà¹à¸à¸¡à¹à¸à¸
â à¹à¸«à¸à¸²ãà¸à¸³à¸à¸§à¸ à¸ªà¸ãà¸ªà¹à¸à¸¡à¹à¸à¸
â à¹à¸à¸ãà¸à¸³à¸à¸§à¸ @ã
â à¹à¸§à¸£à¸±à¸ªãà¸à¸³à¸à¸§à¸ @ãà¸£à¸±à¸ à¸à¸à¹à¸§à¸£à¸±à¸ª
â à¸à¸¥à¸´à¸§ã@ã à¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸°
â à¸ªà¹à¸à¹à¸à¸ã@ãà¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸°
â à¸à¸¸à¸ã@ãà¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸°
â à¸¥à¸­à¸à¸à¸¹ã@ãà¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸°
â à¸¥à¹à¸­à¹à¸¥à¹à¸ã@ãà¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸°
â à¹à¸à¸«à¸³ã@ãà¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸°
â à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ã@ã
â à¸¥à¹à¸²à¸à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ã@ã
â à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ à¹à¸à¸´à¸/à¸à¸´à¸
â à¸¢à¸à¹à¸¥à¸´à¸ ãà¸à¸³à¸à¸§à¸ãà¸¢à¸à¹à¸¥à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡
â âââââââââââââââââââââ
â à¸à¸³à¸ªà¸±à¹à¸à¹à¸à¸´à¸à¸à¸´à¸à¸à¸±à¹à¸à¸«à¸¡à¸:
â âââââââââââââââââââââ
â à¹à¸à¸´à¸à¸à¸/à¸à¸´à¸à¸à¸
â à¹à¸à¸´à¸à¸¡à¸¸à¸à¸¥à¸´à¹à¸/à¸à¸´à¸à¸¡à¸¸à¸à¸¥à¸´à¹à¸
â à¹à¸à¸´à¸à¹à¸à¹à¸²/à¸à¸´à¸à¹à¸à¹à¸²
â à¹à¸à¸´à¸à¸à¸¥à¹à¸­à¸/à¸à¸´à¸à¸à¸¥à¹à¸­à¸
â à¹à¸à¸´à¸à¹à¸­à¸/à¸à¸´à¸à¹à¸­à¸
â à¹à¸à¸´à¸à¸­à¸­à¸à¹à¸à¸/à¸à¸´à¸à¸­à¸­à¸à¹à¸à¸
â à¹à¸à¸´à¸à¸­à¹à¸²à¸/à¸à¸´à¸à¸­à¹à¸²à¸
â à¹à¸à¸´à¸à¹à¸à¸/à¸à¸´à¸à¹à¸à¸
â à¹à¸à¸´à¸à¹à¸à¸à¹à¸à¸/à¸à¸´à¸à¹à¸à¸à¹à¸à¸
â à¹à¸à¸´à¸à¸à¸à¹à¸à¹à¸²/à¸à¸´à¸à¸à¸à¹à¸à¹à¸²
â à¹à¸à¸´à¸à¸à¸à¸­à¸­à¸/à¸à¸´à¸à¸à¸à¸­à¸­à¸
â à¹à¸à¸´à¸à¹à¸à¸à¹à¸à¸°/à¸à¸´à¸à¹à¸à¸à¹à¸à¸°
â à¸à¸´à¹à¸à¹à¸à¸´à¸/à¸à¸´à¹à¸à¸à¸´à¸
â à¹à¸à¸´à¸à¹à¸à¸°à¸à¸à¸¥à¸à¸à¸´à¹à¸/à¸à¸´à¸à¹à¸à¸°à¸à¸à¸¥à¸à¸à¸´à¹à¸
â à¹à¸à¸´à¸à¹à¸­à¸/à¸à¸´à¸à¹à¸­à¸
â à¹à¸à¸´à¸à¹à¸­à¸à¸­à¹à¸²à¸/à¸à¸´à¸à¹à¸­à¸à¸­à¹à¸²à¸
â âââââââââââââââââââââ
â à¸à¸³à¸ªà¸±à¹à¸à¸à¹à¸²à¸à¸±à¹à¸à¸«à¸¡à¸ :
â âââââââââââââââââââââ
â à¸à¸±à¹à¸à¸­à¹à¸²à¸1ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¸­à¹à¸²à¸2ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸
â à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸
â à¸à¸±à¹à¸à¸à¸à¹à¸­à¸:ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¸
â à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¸
â à¸à¸±à¹à¸à¹à¸à¸:ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¹à¸à¸à¹à¸à¸:ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸
â à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸
â à¸à¸±à¹à¸à¸à¸à¹à¸­à¸:ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¸­à¸­à¸
â à¸¥à¸à¸à¸´à¹à¸à¸à¸à¸­à¸­à¸
â à¸à¸±à¹à¸à¸à¸à¸­à¸­à¸:ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¹à¸²
â à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¹à¸²
â à¸à¸±à¹à¸à¸à¸à¹à¸à¹à¸²:ãà¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸µà¹à¸à¹à¸­à¸à¸à¸²à¸£ã
â âââââââââââââââââââââ 
"""
helpmusic ="""ã Music ã

â¢ Key:  Musicãqueryã
â¢ Detail Music
â¢ Key:  Music ãquery | num ã"""
helpbio ="""ã Biography ã

â¢ Key:  Biographyãqueryã
â¢ Detail Biography
â¢ Key:  Biographyãquery numã"""
helptrans= """ã TransLator ã

â¢ af : Afrikaans
â¢ sq : Albanian
â¢ ar : Arabic
â¢ hy : Armenian
â¢ bn : Bengali
â¢ ca : Catalan
â¢ zh : Chinese
â¢ zhcn : Chinese
â¢ zhtw : Chinese
â¢ zhyue : Chinese
â¢ hr : Croatian
â¢ cs : Czech
â¢ da : Danish
â¢ nl : Dutch
â¢ en : English
â¢ enau : English
â¢ enuk : English
â¢ enus : English
â¢ eo : Esperanto
â¢ fi : Finnish
â¢ fr : French
â¢ de : German
â¢ el : Greek
â¢ hi : Hindi
â¢ hu : Hungarian
â¢ s : Icelandic
â¢ id : Indonesian
â¢ it : Italian
â¢ ja : Japanese
â¢ km : Khme
â¢ ko : Korean
â¢ la : Latin
â¢ lv : Latvian
â¢ mk : Macedonian
â¢ no : Norwegian
â¢ pl : Polish
â¢ pt : Portuguese
â¢ ro : Romanian
â¢ ru : Russian
â¢ sr : Serbian
â¢ si : Sinhala
â¢ sk : Slovak
â¢ es : Spanish
â¢ eses : Spanish
â¢ esus : Spanish
â¢ sw : Swahili
â¢ sv : Swedish
â¢ ta : Tamil
â¢ th : Thai
â¢ tr : Turkish
â¢ uk : Ukrainian
â¢ vi : Vietnamese
example :
tr-en saya tampan
say-en saya keren"""
#==============================================================================================================
#==============================================================================================================
#=============================================[ OPERATION STARTED ]============================================
#==============================================================================================================
def lineBot(op):
    try:
        if op.type == 0:
            return
#==============================================================================================================
#=============================================[OP TYPE 5 AUTO ADD]=============================================
#==============================================================================================================
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                client.findAndAddContactsByMid(op.param1)
            if settings["autoBlock"] == True:
                client.blockContact(op.param1) 
            msgSticker = settings["messageSticker"]["listSticker"]["addSticker"]
            if msgSticker != None:
                sid = msgSticker["STKID"]
                spkg = msgSticker["STKPKGID"]
                sver = msgSticker["STKVER"]
                sendSticker(op.param1, sver, spkg, sid)
            if "@!" in settings["addPesan"]:
                msg = settings["addPesan"].split("@!")
                return sendMention(op.param1, op.param1, msg[0], msg[1])
            sendMention(op.param1, op.param1, "Halo", ", {}".format(str(settings['addPesan'])))
            arg = "   New Friend : {}".format(str(client.getContact(op.param1).displayName))
            print (arg)

        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
            group = client.getGroup(op.param1)
            contact = client.getContact(op.param2)
            if settings["autoJoin"] and clientMID in op.param3:
                client.acceptGroupInvitation(op.param1)
                sendMention(op.param1, op.param2, "Hello", ", thanks for invite me")
                
        if op.type == 13:
            print(op.param1)
            print(op.param2)
            print(op.param3)
            if mid in op.param3:
                G = client.getGroup(op.param1)
                if setting["autoJoin"] == True:
                    if setting["autoCancel"]["on"] == True:
                        if len(G.members) <= setting["autoCancel"]["members"]:
                            client.rejectGroupInvitation(op.param1)
                        else:
                            client.acceptGroupInvitation(op.param1)
                    else:
                        client.acceptGroupInvitation(op.param1)
                elif setting["autoCancel"]["on"] == True:
                    if len(G.members) <= setting["autoCancel"]["members"]:
                        client.rejectGroupInvitation(op.param1)
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                matched_list = []
                for tag in setting["blacklist"]:
                    matched_list+=filter(lambda str: str == tag, InviterX)
                if matched_list == []:
                    pass
                else:
                    client.cancelGroupInvitation(op.param1, matched_list)

#==============================================================================================================
#==============================================[OP TYPE 13 JOIN]===============================================
#==============================================================================================================
#==============================================================================================================
#==============================================================================================================
        if op.type == 15:
            print ("[ 15 ]  NOTIFIED LEAVE GROUP")
            if settings["leaveMessage"] == True:
                if "{gname}" in settings['leavePesan']:
                    gName = client.getGroup(op.param1).name
                    msg = settings['leavePesan'].replace("{gname}", gName)
                    msgSticker = settings["messageSticker"]["listSticker"]["leaveSticker"]
                    if msgSticker != None:
                        sid = msgSticker["STKID"]
                        spkg = msgSticker["STKPKGID"]
                        sver = msgSticker["STKVER"]
                        sendSticker(op.param2, sver, spkg, sid)
                    if "@!" in settings['leavePesan']:
                        msg = msg.split("@!")
                        return sendMention(op.param2, op.param2, msg[0], msg[1])
                    return sendMention(op.param2, op.param2, "Hallo ", msg)
                msgSticker = settings["messageSticker"]["listSticker"]["leaveSticker"]
                if msgSticker != None:
                    sid = msgSticker["STKID"]
                    spkg = msgSticker["STKPKGID"]
                    sver = msgSticker["STKVER"]
                    sendSticker(op.param1, sver, spkg, sid)
                sendMention(op.param1, op.param2, "Bye", "\n{}".format(str(settings['leavePesan'])))

        if op.type == 17:
            print ("[ 17 ]  NOTIFIED ACCEPT GROUP INVITATION")
            if settings["welcomeMessage"] == True:
                group = client.getGroup(op.param1)
                contact = client.getContact(op.param2)
                msgSticker = settings["messageSticker"]["listSticker"]["welcomeSticker"]
                if msgSticker != None:
                    sid = msgSticker["STKID"]
                    spkg = msgSticker["STKPKGID"]
                    sver = msgSticker["STKVER"]
                    sendSticker(op.param1, sver, spkg, sid)
                if "{gname}" in settings['welcomePesan'].lower():
                    gName = group.name
                    msg = settings['welcomePesan'].replace("{gname}", gName)
                    if "@!" in msg:
                        msg = msg.split("@!")
                        return sendMention(op.param1, op.param2, msg[0], msg[1])
                    sendMention(op.param1, op.param2, "à¸ªà¸§à¸±à¸ªà¸à¸µà¸à¸£à¹à¸²", msg)
                else:
                    sendMention(op.param1, op.param2, "à¸ªà¸§à¸±à¸ªà¸à¸µà¸à¸£à¹à¸²","\n{}".format(str(settings['welcomePesan'])))
                    contact = client.getContact(op.param2)
                    client.sendImageWithURL(op.param1,image)
                    arg = "   Group Name : {}".format(str(group.name))
                    arg += "\n   User Join : {}".format(str(contact.displayName))
                    print (arg)
#==============================================================================================================
#==============================================[OP TYPE 22 24 JOIN]============================================
#==============================================================================================================
        if op.type == 22:
            print ("[ 22 ] NOTIFIED INVITE INTO ROOM")
            if settings["autoLeave"] == True:
                client.sendMessage(op.param1, "ngapain invite gw -,-")
                client.leaveRoom(op.param1)

        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                client.sendMessage(op.param1, "Goblok ngapain invite gw")
                client.leaveRoom(op.param1)
        if op.type in [25,26]:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 2:
                if msg.toType == 0:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.contentType == 0:
                    if text is None:
                        return
                    else:
                        cmd = command(text)
                        if msg.text:
                            if msg.text.lower().lstrip().rstrip() in wbanlist:
                                if msg.text not in clientMID:
                                    try:
                                        client.kickoutFromGroup(msg.to,[sender])
                                    except Exception as e:
                                        print(e)
                        if receiver in temp_flood:
                            if temp_flood[receiver]["expire"] == True:
                               if cmd == "open":
                                    temp_flood[receiver]["expire"] = False
                                    temp_flood[receiver]["time"] = time.time()
                                    client.sendMessage(to,"Bot Actived")
                               return
                            elif time.time() - temp_flood[receiver]["time"] <= 5:
                                temp_flood[receiver]["flood"] += 1
                                if temp_flood[receiver]["flood"] >= 20:
                                    temp_flood[receiver]["flood"] = 0
                                    temp_flood[receiver]["expire"] = True
                                    ret_ = "I will be off for 30 seconds, type open to re-enable"
                                    userid = "https://line.me/ti/p/~" + client.profile.userid
                                    client.sendFooter(to, "Flood Detect !\n"+str(ret_), str(userid), "http://dl.profile.line-cdn.net/"+client.getContact(clientMID).pictureStatus, client.getContact(clientMID).displayName)
                            else:
                                 temp_flood[receiver]["flood"] = 0
                            temp_flood[receiver]["time"] = time.time()
                        else:
                            temp_flood[receiver] = {
    	                        "time": time.time(),
    	                        "flood": 0,
    	                        "expire": False
                            }

        if op.type == 26:
#            if settings ["mutebot2"] == True:
            msg = op.message
            try:
                if msg.toType == 0:
                    client.log("[%s]"%(msg._from)+str(msg.text))
                else:
                    group = client.getGroup(msg.to)
                    contact = client.getContact(msg._from)
                    client.log("[%s]"%(msg.to)+"\nGroupname: "+str(group.name)+"\nNamenya: "+str(contact.displayName)+"\nPesannya: "+str(msg.text))
                if msg.contentType == 0:
            #Save message to dict
                    msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                if msg.contentType == 7:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "="
                    ret_ += "\nSTICKER ID : {}".format(stk_id)
                    ret_ += "\nSTICKER PACKAGES ID : {}".format(pkg_id)
                    ret_ += "\nSTICKER VERSION : {}".format(stk_ver)
                    ret_ += "\nSTICKER URL : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n"
                    msg_dict[msg.id] = {"text":str(ret_),"from":msg._from,"createdTime":msg.createdTime}
            except Exception as e:
                print(e)
#==============================================================================================================
        if op.type == 25:
#             if settings ["mutebot2"] == True:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sam = squareChatMid
            sender = msg._from
            if msg.toType == 0:
                if sender != client.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
                elif msg.text.lower().startswith("à¸à¸±à¹à¸à¸­à¹à¸²à¸1 "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    settings["anu"] = str(say).lower()
                    client.sendMessage(msg.to, "à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¹à¸²à¸ ã " + str(settings["anu"]) + " ã")
                elif msg.text.lower().startswith("à¸à¸±à¹à¸à¸­à¹à¸²à¸2 "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    settings["anu2"] = str(say).lower()
                    client.sendMessage(msg.to, "à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¹à¸²à¸ ã " + str(settings["anu2"]) + " ã")
                elif msg.text.lower().startswith("say "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    client.sendMessage(to, (say))
                    assist.sendMessage(to, (say))
                    kicker.sendMessage(to, (say))
                    kicker2.sendMessage(to, (say))
#==============================================================================================================
                elif text.lower() == "à¸à¸³à¸ªà¸±à¹à¸" or text.lower() == ".":
                    helpmessagee = helpmsg
                    client.sendMessage(to, str(helpmessagee))
                elif text.lower() == "self" or text.lower() == ".":
                    helpselfbot = helpself
                    client.sendMessage(to, str(helpselfbot))
                elif text.lower() == "fiture" or text.lower() == ".":
                    helpftr = helpfiture
                    client.sendMessage(to, str(helpftr))
                elif text.lower() == "update" or text.lower() == ".":
                    helpup = helpupdate
                    client.sendMessage(to, str(helpup))
                elif text.lower() == "group" or text.lower() == ".":
                    helpgc = helpgroup
                    client.sendMessage(to, str(helpgc))
                elif text.lower() == "reader" or text.lower() == ".":
                    helprd = helpread
                    client.sendMessage(to, str(helprd))
                elif text.lower() == "author" or text.lower() == ".":
                    helpaut = helpauthor
                    client.sendMessage(to, str(helpaut))
                elif text.lower() == "stealing" or text.lower() == ".":
                    helpst = helpsteal
                    client.sendMessage(to, str(helpst))
                elif text.lower() == "spaming" or text.lower() == ".":
                    helpsp = helpspam
                    client.sendMessage(to, str(helpsp))
                elif text.lower() == "settings" or text.lower() == ".":
                    helpsett = helpset
                    client.sendMessage(to, str(helpsett))
                elif text.lower() == "banning" or text.lower() == ".":
                    helpbn = helpban
                    client.sendMessage(to, str(helpbn))
                elif text.lower() == "translate" or text.lower() == ".":
                    helptr = helptrans
                    client.sendMessage(to, str(helptr))
                elif text.lower() == "lyric" or text.lower() == ".":
                    helply= helplyric
                    client.sendMessage(to, str(helply))
                elif text.lower() == "youtube" or text.lower() == ".":
                    helpyt = helpytube
                    client.sendMessage(to, str(helpyt))
                elif text.lower() == "camera" or text.lower() == ".":
                    helpcm = helpcam
                    client.sendMessage(to, str(helpcm))
                elif text.lower() == "music" or text.lower() == ".":
                    helpmc = helpmusic
                    client.sendMessage(to, str(helpmc))
                elif text.lower() == "kaskus" or text.lower() == ".":
                    helpks = helpkus
                    client.sendMessage(to, str(helpks))
                elif text.lower() == "soundcloud" or text.lower() == ".":
                    helpsd = helpsound
                    client.sendMessage(to, str(helpsd))
                elif text.lower() == "news" or text.lower() == ".":
                    helpnw = helpnews
                    client.sendMessage(to, str(helpnw))
                elif text.lower() == "province" or text.lower() == ".":
                    helppv = helpprov
                    client.sendMessage(to, str(helppv))
                elif text.lower() == "brainly" or text.lower() == ".":
                    helpbr = helpbran
                    client.sendMessage(to, str(helpbr))
                elif text.lower() == "lyric" or text.lower() == ".":
                    helprik = helpry
                    client.sendMessage(to, str(helprik))
                elif msg.text.lower().startswith("contact "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    client.sendMessage(receiver, None, contentMetadata={'mid': say}, contentType=13)
#==============================================================================================================
#==============================================================================================================
#==============================================================================================================
                elif msg.text.lower() == "invite:on":
                    if msg._from in clientMID:
                        settings["winvite"] = True
                        client.sendMessage(msg.to,"Send Contact to Invite")
#==============================================================================================================
                elif "à¸ªà¹à¸à¹à¸à¸ " in msg.text:
                    if msg._from in clientMID:                                                                                                                                       
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]                                                                                                                                
                        targets = []
                        for x in key["MENTIONEES"]:                                                                                                                                  
                            targets.append(x["M"])
                        for target in targets:                                                                                                                                       
                            try:
                                client.kickoutFromGroup(msg.to,[target])
                            except:
                                pass
                elif "à¸à¸¸à¸ " in msg.text:
                    if msg._from in clientMID:                                                                                                                                       
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]                                                                                                                                
                        targets = []
                        for x in key["MENTIONEES"]:                                                                                                                                  
                            targets.append(x["M"])
                        for target in targets:                                                                                                                                       
                            try:
                                client.kickoutFromGroup(msg.to,[target])
                                client.inviteIntoGroup(msg.to,[target])
                                client.cancelGroupInvitation(msg.to,[target])
                            except:
                                pass
                elif "Invite " in msg.text:
                    if msg._from in clientMID:                                                                                                                                       
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]                                                                                                                                
                        targets = []
                        for x in key["MENTIONEES"]:                                                                                                                                  
                            targets.append(x["M"])
                        for target in targets:                                                                                                                                       
                            try:
                                client.findAndAddContactsByMid(target)
                                client.inviteIntoGroup(msg.to,[target])
                            except:
                                pass
#==============================================================================================================
                elif msg.text.lower().startswith("say-af "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'af'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-sq "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sq'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-ar "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ar'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-hy "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hy'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-bn "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'bn'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-ca "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ca'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-zh "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-zh-cn "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-cn'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-zh-tw "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-tw'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-zh-yue "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'zh-yue'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-hr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-cs "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'cs'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-da "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'da'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-nl "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'nl'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-en "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-en-au "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en-au'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-en-uk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en-uk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-en-us "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'en-us'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-eo "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'eo'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-fi "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'fi'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-fr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'fr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-de "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'de'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-el "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'el'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-hi "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hi'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-hu "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'hu'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-is "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'is'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-id "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'id'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-it "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'it'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-ja "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ja'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-km "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'km'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-ko "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ko'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-la "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'la'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-lv "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'lv'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-mk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'mk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-no "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'no'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-pl "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'pl'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-pt "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'pt'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-do "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ro'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-ru "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ru'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-sr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-si "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'si'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-sk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-es "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'es'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-es-es "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'es-es'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-es-us "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'es-us'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-sw "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sw'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-sv "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'sv'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-ta "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'ta'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("à¸à¸¹à¸ "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'th'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-tr "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'tr'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-uk "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'uk'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-vi "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'vi'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
                elif msg.text.lower().startswith("say-cy "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'cy'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    client.sendAudio(msg.to,"hasil.mp3")
#==============================================================================================================
                elif msg.text.lower().startswith("tr-af "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='af')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sq "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sq')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-am "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='am')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ar "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ar')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hy "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hy')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-az "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='az')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-eu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='eu')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-be "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='be')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-bn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='bn')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-bs "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='bs')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-bg "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='bg')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ca "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ca')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ceb "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ceb')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ny "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ny')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-zh-cn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zh-cn')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-zh-tw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zh-tw')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-co "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='co')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hr')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-cs "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='cs')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-da "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='da')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-nl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='nl')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-en "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='en')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-et "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='et')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fi')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fr')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fy "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fy')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-gl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='gl')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ka "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ka')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-de "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='de')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-el "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='el')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-gu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='gu')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ht "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ht')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ha "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ha')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-haw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='haw')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-iw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='iw')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hi')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hmn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hmn')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-hu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='hu')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-is "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='is')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ig "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ig')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-id "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='id')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ga "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ga')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-it "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='it')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ja "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ja')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-jw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='jw')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-kn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='kn')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-kk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='kk')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-km "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='km')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ko "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ko')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ku "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ku')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ky "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ky')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lo "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lo')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-la "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='la')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lv "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lv')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lt "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lt')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-lb "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='lb')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mk')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mg "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mg')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ms "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ms')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ml "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ml')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mt "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mt')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mi')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mr')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-mn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='mn')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-my "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='my')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ne "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ne')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-no "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='no')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ps "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ps')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fa "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fa')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-pl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='pl')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-pt "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='pt')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-pa "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='pa')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ro "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ro')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ru "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ru')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sm "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sm')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-gd "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='gd')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sr')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-st "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='st')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sn "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sn')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sd "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sd')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-si "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='si')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sk')
                    A = hasil.text
                    line.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sl "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sl')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-so "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='so')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-es "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='es')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-su "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='su')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sw "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sw')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-sv "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='sv')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-tg "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='tg')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ta "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ta')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-te "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='te')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-th "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='th')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-tr "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='tr')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-uk "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='uk')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-ur "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='ur')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-uz "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='uz')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-vi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='vi')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-cy "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='cy')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-xh "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='xh')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-yi "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='yi')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-yo "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='yo')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-zu "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='zu')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-fil "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='fil')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower().startswith("tr-he "):
                    sep = text.split(" ")
                    isi = text.replace(sep[0] + " ","")
                    translator = Translator()
                    hasil = translator.translate(isi, dest='he')
                    A = hasil.text
                    client.sendMessage(msg.to, A)
                elif msg.text.lower() == "à¹à¸à¸´à¸à¹à¸à¸":
                    settings["detectMention"] = True
                    client.sendMessage(msg.to,"à¹à¸à¸´à¸à¹à¸à¸à¹à¸£à¸µà¸à¸£à¹à¸­à¸¢à¸à¸£à¸±à¸")
                elif msg.text.lower() == "à¸à¸´à¸à¹à¸à¸":
                    settings["detectMention"] = False
                    client.sendMessage(msg.to,"à¸à¸´à¸à¹à¸à¸à¹à¸£à¸µà¸à¸£à¹à¸­à¸¢à¸à¸£à¸±à¸")
                elif msg.text.lower() == "à¹à¸à¸´à¸à¹à¸à¸à¹à¸à¸":
                    settings["detectMentionPM"] = True
                    client.sendMessage(msg.to,"à¹à¸à¸´à¸à¹à¸à¸à¹à¸à¸à¹à¸£à¸µà¸¢à¸à¸£à¹à¸­à¸¢à¸à¸£à¸±à¸")
                elif msg.text.lower() == "à¸à¸´à¸à¹à¸à¸à¹à¸à¸":
                    settings["detectMentionPM"] = False
                    client.sendMessage(msg.to,"à¸à¸´à¸à¹à¸à¸à¹à¸à¸à¹à¸£à¸µà¸¢à¸à¸£à¹à¸­à¸¢à¸à¸£à¸±à¸")
                elif msg.text.lower().startswith("à¸à¸±à¹à¸à¹à¸à¸à¹à¸à¸: "):
                    text = msg.text.lower().replace("à¸à¸±à¹à¸à¹à¸à¸à¹à¸à¸: ","")
                    settings["pmMessage"] = text
                    client.sendMessage(msg.to, "à¸à¸³à¹à¸à¸à¹à¸à¸ à¸ªà¸ à¸à¸·à¸­ : {}".format(str(settings["pmMessage"])))
                elif msg.text.lower().startswith("setrespongroup: "):
                    text = msg.text.lower().replace("setrespongroup: ","")
                    settings["respMessage"] = text
                    client.sendMessage(msg.to, "Success Update Response Group to : {}".format(str(settings["respMessage"])))
#==============================================================================================================
        if op.type == 26:
 #            if settings ["mutebot2"] == True:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 2:
                if msg.toType == 0:
                    to = sender
                elif msg.toType == 2:
                    to = receiver
                if settings["autoRead"] == True:
                    client.sendChatChecked(to, msg_id)
                if msg.contentType == 0:
                    if settings["unsendMessage"] == True:
                        try:
                            if msg.location != None:
                                unsendmsg = time.time()
                                msg_dict[msg.id] = {"lokasi":msg.location,"from":msg._from,"waktu":unsendmsg}
                            else:
                                unsendmsg = time.time()
                                msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"waktu":unsendmsg}
                        except Exception as e:
                            print (e)
                if msg.contentType == 1:
                    if settings["unsendMessage"] == True:
                        try:
                            unsendmsg1 = time.time()
                            path = client.downloadObjectMsg(msg_id)
                            msg_dict[msg.id] = {"from":msg._from,"image":path,"waktu":unsendmsg1}
                        except Exception as e:
                            print (e)
                if msg.contentType == 2:
                    if settings["unsendMessage"] == True:
                        try:
                            unsendmsg2 = time.time()
                            path = client.downloadObjectMsg(msg_id)
                            msg_dict[msg.id] = {"from":msg._from,"video":path,"waktu":unsendmsg2}
                        except Exception as e:
                            print (e)
                if msg.contentType == 3:
                    if settings["unsendMessage"] == True:
                        try:
                            unsendmsg3 = time.time()
                            path = client.downloadObjectMsg(msg_id)
                            msg_dict[msg.id] = {"from":msg._from,"audio":path,"waktu":unsendmsg3}
                        except Exception as e:
                            print (e)
                if msg.contentType == 7:
                    if settings["unsendMessage"] == True:
                        try:
                            unsendmsg7 = time.time()
                            sticker = msg.contentMetadata["STKID"]
                            link = "http://dl.stickershop.line.naver.jp/stickershop/v1/sticker/{}/android/sticker.png".format(sticker)
                            msg_dict[msg.id] = {"from":msg._from,"sticker":link,"waktu":unsendmsg7}
                        except Exception as e:
                            print (e)
                if msg.contentType == 13:
                    if settings["unsendMessage"] == True:
                        try:
                            unsendmsg13 = time.time()
                            mid = msg.contentMetadata["mid"]
                            msg_dict[msg.id] = {"from":msg._from,"mid":mid,"waktu":unsendmsg13}
                        except Exception as e:
                            print (e)
                if msg.contentType == 14:
                    if settings["unsendMessage"] == True:
                        try:
                            unsendmsg14 = time.time()
                            path = client.downloadObjectMsg(msg_id)
                            msg_dict[msg.id] = {"from":msg._from,"file":path,"waktu":unsendmsg14}
                        except Exception as e:
                            print (e)
#==============================================================================================================
                if msg.toType == 0 and settings["autoReply"] and sender != clientMID:
                    contact = client.getContact(sender)
                    rjct = ["auto", "ngetag"]
                    validating = [a for a in rjct if a.lower() in text.lower()]
                    if validating != []: return
                    if contact.attributes != 32:
                        msgSticker = settings["messageSticker"]["listSticker"]["sleepSticker"]
                        if msgSticker != None:
                            sid = msgSticker["STKID"]
                            spkg = msgSticker["STKPKGID"]
                            sver = msgSticker["STKVER"]
                            sendSticker(to, sver, spkg, sid)
                        if "@!" in settings["replyPesan"]:
                            msg_ = settings["replyPesan"].split("@!")
                            sendMention(to, sender, "Sleep Mode :\n" + msg_[0], msg_[1])
                        sendMention(to, sender, "Sleep Mode :\nà¸à¹à¸°à¹à¸­à¹", settings["replyPesan"])
                if 'MENTION' in msg.contentMetadata.keys()!= None:
                    if settings["detectMentionPM"] == True:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            if clientMID in mention["M"]:
                                sendMention(sender, sender, "ãà¸à¸­à¸à¹à¸à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ã\n", "\n" + str(settings["pmMessage"]))
                                break
                if msg.contentType == 0: 
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        gInfo = client.getGroup(receiver)
                        members = gInfo.members
                        if len(members) == len(mentionees): return
                        elif "list user" in text.lower(): return
                        elif len(mentionees) >= 50: return
                        for mention in mentionees:
                            if clientMID in mention["M"]:
                                rjct = ["auto", "ngetag"]
                                if settings["detectMention"] == True:
                                    msgSticker = settings["messageSticker"]["listSticker"]["responSticker"]
                                    if msgSticker != None:
                                        sid = msgSticker["STKID"]
                                        spkg = msgSticker["STKPKGID"]
                                        sver = msgSticker["STKVER"]
                                        sendSticker(to, sver, spkg, sid)
                                    if "@!" in settings["mentionPesan"]:
                                        msg_ = settings["mentionPesan"].split("@!")
                                        return sendMention(to, sender, "à¸à¹à¸­à¸à¸§à¸²à¸¡à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´\n" + msg_[0], msg_[1])
                                    sendMention(receiver, sender, "ð" ,"\n{}".format(str(settings['mentionPesan'])))
                                break
                if 'MENTION' in msg.contentMetadata.keys() != None:
                    if settings["notag"] == True:
                        name = re.findall(r'@(\w+)', msg.text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            if clientMID in mention["M"]:
                               client.sendMessage(msg.to, "à¸à¸­à¸à¹à¸¥à¹à¸§à¸­à¸¢à¹à¸²à¹à¸à¸à¹à¸¢à¸­à¸°à¸à¸¸à¸à¹à¸¥à¸¢5555")
                               client.kickoutFromGroup(msg.to, [msg._from])
                               break
#==============================================================================================================
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
#==============================================================================================================
                if msg.contentType == 0:
                    if msg.toType == 0:
                        if settings["responpm"] == True:
                            sendMention(sender, sender, "à¸à¹à¸°à¹à¸­à¹", "saya sedang offline, PM nanti :)")
#==============================================================================================================
                if msg.contentType == 13:
                    if settings["checkContact"] == True:
                        msg.contentType = 0
                        client.sendMessage(msg.to,msg.contentMetadata["mid"])
                        if 'displayName' in msg.contentMetadata:
                            contact = client.getContact(msg.contentMetadata["mid"])
                            try:
                                cu = channel.getProfileCoverURL(msg.contentMetadata["mid"])
                            except:
                                cu = ""
                            client.sendMessage(msg.to,"ãDisplayNameã:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                        else:
                            contact = client.getContact(msg.contentMetadata["mid"])
                            try:
                                cu = channel.getProfileCoverURL(msg.contentMetadata["mid"])
                            except:
                                cu = ""
                            if settings["server"] == "VPS":
                                client.sendMessage(msg.to,"ãDisplayNameã:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                                client.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + contact.pictureStatus)
                                client.sendImageWithURL(msg.to,str(cu))
#==============================================================================================================
#==========================================[ SCRIPT SELF START ]===============================================
#==============================================================================================================
        if op.type == 25:
#             if settings ["mutebot2"] == True:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 2:
                if msg.toType == 0:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.contentType == 0:
                    if settings["autoRead"] == True:
                        client.sendChatChecked(to, msg_id)
                    if text is None:
                        return
                    else:
                        cmd = command(text)
                    if cmd != "Undefined command":
#==============================================================================================================
                        if cmd == "tts":
                            texttospeech = helptexttospeech()
                            client.sendMessage(to, str(texttospeech))
                        elif cmd == "translate":
                            helpTranslate = helptranslate()
                            client.sendMessage(to, str(helpTranslate))
                        elif cmd == "restart" or cmd == "reboot":
                            client.sendMessage(to, "Succes logout from bots")
                            settings["restartPoint"] = to
                            restartBot()
                        elif cmd == "à¸à¸" or cmd == "tes":
                            client.sendMentionFooter(to, 'ãà¹à¸£à¸²ã\n', sender, "https://line.me/ti/p/~yukie2k18", "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName);client.sendMessage(to, client.getContact(sender).displayName, contentMetadata = {'previewUrl': 'http://dl.profile.line-cdn.net/'+client.getContact(sender).pictureStatus, 'i-installUrl': 'https://line.me/ti/p/~guarmselfbot1122', 'type': 'mt', 'subText': "armselfbot", 'a-installUrl': 'https://line.me/ti/p/~guarmselfbot1122', 'a-installUrl': ' https://line.me/ti/p/~guarmselfbot1122', 'a-packageName': 'com.spotify.music', 'countryCode': 'ID', 'a-linkUri': 'https://line.me/ti/p/~guarmselfbot1122', 'i-linkUri': 'https://line.me/ti/p/~guarmselfbot1122', 'id': 'mt000000000a6b79f9', 'text': 'Khie', 'linkUri': 'https://line.me/ti/p/~guarmselfbot1122'}, contentType=19)
                        elif cmd == "yabi":
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, str(userid), "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                            client.sendMentionFooter(to, 'ãMeã\n', sender, str(userid), "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                            client.sendMusic(to, client.getContact(sender).displayName, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, str(userid), "Khie Bot", client.getContact(sender).displayName)
                        elif cmd == "speed":
                            start = time.time()
                            client.sendMessage(to, "Counting...")
                            speed = time.time() - start
                            ping = speed * 1000
                            client.sendMessage(to, "The result is {} ms".format(str(speedtest(ping))))
                        elif cmd == "newticket":
                            client.reissueUserTicket()
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendFooter(to, "ãNew Ticketã\n"+str(userid), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "ticket":
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendFooter(to, "ãTicketã\n"+str(userid), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "getannounce":
                            gett = client.getChatRoomAnnouncements(receiver)
                            for a in gett:
                                aa = client.getContact(a.creatorMid).displayName
                                bb = a.contents
                                cc = bb.link
                                textt = bb.text
                                client.sendMessage(to, 'Link: ' + str(cc) + '\nText: ' + str(textt) + '\nCreator: ' + str(aa))
                        elif cmd == "à¸­à¸­à¸":
                            timeNow = time.time()
                            runtime = timeNow - botStart
                            runtime = format_timespan(runtime)
                            resetTime = timeNow - int(settings["timeRestart"])
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendFooter(to, "ãà¹à¸§à¸¥à¸²à¸à¸³à¸à¸²à¸à¸à¸­à¸à¸à¸­à¸ã\n{} ".format(str(runtime)), str(userid), "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "à¹à¸à¸":
                            client.sendMessage(to, text=None, contentMetadata=None, contentType=9)
                        elif cmd == "à¸­à¸±à¸à¸£à¸¹à¸":
                            settings["changePicture"] = True
                            sendMention(to, sender, "ã à¹à¸à¸¥à¸µà¹à¸¢à¸à¸£à¸¹à¸à¸ªà¸³à¹à¸£à¹à¸à¹à¸¥à¹à¸§ã\nâ¢", "\nSend pict !")
                        elif cmd == "à¸­à¸±à¸à¸§à¸µà¸à¸µà¹à¸­" and sender == clientMID:
                            settings['changeProfileVideo']['status'] = True
                            settings['changeProfileVideo']['stage'] = 1
                            sendMention(to, sender, "ã à¹à¸à¸¥à¸µà¸¢à¸à¸§à¸µà¸à¸µà¹à¸­à¸ªà¸³à¹à¸£à¹à¸à¹à¸¥à¹à¸§ ã\nâ¢", "\nSend video !")
                        elif cmd == "à¸­à¸±à¸à¸£à¸¹à¸à¸à¸¥à¸¸à¹à¸¡":
                            if msg.toType == 2:
                                if to not in settings["changeGroupPicture"]:
                                    settings["changeGroupPicture"].append(to)
                            sendMention(to, sender, "ã à¸ªà¹à¸à¸£à¸¹à¸à¸à¸µà¹à¸à¸°à¹à¸à¸¥à¸µà¹à¸¢à¸à¸¥à¸à¸¡à¸² ã\nâ¢", "\nà¸à¸±à¹à¸à¸£à¸¹à¸à¸à¸¥à¸¸à¹à¸¡ !")
                        elif cmd.startswith("à¸­à¸±à¸à¸à¸·à¹à¸­ "):
                            string = cmd.replace("à¸­à¸±à¸à¸à¸·à¹à¸­", "")
                            if len(string) <= 10000000000:
                                pname = client.getContact(sender).displayName
                                profile = client.getProfile()
                                profile.displayName = string
                                client.updateProfile(profile)
                                userid = "https://line.me/ti/p/~" + client.profile.userid
                                client.sendFooter(to, "Update Name\nStatus : Success\nFrom : "+str(pname)+"\nTo :"+str(string), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd.startswith("à¸­à¸±à¸à¸à¸±à¸ª "):
                            string = cmd.replace("à¸­à¸±à¸à¸à¸±à¸ª", "")
                            if len(string) <= 10000000000:
                                pname = client.getContact(sender).statusMessage
                                profile = client.getProfile()
                                profile.statusMessage = string
                                client.updateProfile(profile)
                                userid = "https://line.me/ti/p/~" + client.profile.userid
                                client.sendFooter(to, "Update Status\nStatus : Success\nFrom : "+str(pname)+"\nTo :"+str(string), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
#==============================================================================================================
                        elif cmd == "à¹à¸­à¸à¸µà¹à¸£à¸²":
                            userid = "https://line.me/ti/p/" + client.getUserTicket().id
                            client.sendFooter(to, "Mid :\n"+str(sender), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "à¹à¸à¸£à¹à¸£à¸²":
                            contact = client.getContact(clientMID)
                            cu = client.getProfileCoverURL(clientMID)
                            path = str(cu)
                            image = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendImageWithFooter(to, image, userid, image, client.getContact(sender).displayName)
                            client.sendImageWithFooter(to, path, userid, path, client.getContact(sender).displayName)
                            client.sendFooter(to, "My Profile\nMid : "+str(sender)+"\nName : "+str(contact.displayName)+"\nStatus :\n"+str(contact.statusMessage), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "à¸à¸´à¹à¸­à¹à¸£à¸²":
                            h = client.getContact(clientMID)
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendFooter(to, "Name :\n"+str(h.displayName), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "à¸à¸±à¸ªà¹à¸£à¸²":
                            h = client.getContact(clientMID)
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendFooter(to, "Status :\n"+str(h.statusMessage), userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "à¸à¸´à¸ªà¹à¸£à¸²":
                            h = client.getContact(clientMID)
                            image = "http://dl.profile.line-cdn.net/" + h.pictureStatus
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendImageWithFooter(to, image, userid, image, client.getContact(sender).displayName)
                        elif cmd == "à¸§à¸µà¸à¸µà¹à¸­à¹à¸£à¸²":
                            userid = "https://line.me/ti/p/" + client.getUserTicket().id
                            h = client.getContact(clientMID)
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            if h.videoProfile == None:
                            	return client.sendFooter(to, " Video\nNone", userid, "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                            client.sendVideoWithFooter(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus + "/vp", str(userid), "http://dl.profile.line-cdn.net/"+client.getContact(sender).pictureStatus, client.getContact(sender).displayName)
                        elif cmd == "à¸à¸à¹à¸£à¸²":
                            h = client.getContact(clientMID)
                            cu = client.getProfileCoverURL(clientMID)
                            image = str(cu)
                            userid = "https://line.me/ti/p/~" + client.profile.userid
                            client.sendImageWithFooter(to, image, userid, image, client.getContact(sender).displayName)
                        elif cmd == "clear invite":
                            ginvited = client.getGroupIdsInvited()
                            if ginvited != [] and ginvited != None:
                                for gid in ginvited:
                                    client.rejectGroupInvitation(gid)
                                client.sendMessage(to, "Reject {} Group invitation".format(str(len(ginvited))))
                            else:
                                client.sendMessage(to, "")
#==============================================================================================================
                        elif cmd == 'à¹à¸­à¸à¸µ':
                            client.sendMessage(to,"ã MID ã\n" +  to)
                        elif cmd == 'Me':
                            client.sendMessage(to, text=None, contentMetadata={'mid': receiver}, contentType=13)
                        elif cmd == 'à¸à¸·à¹à¸­':
                            me = client.getContact(to)
                            client.sendMessage(to,"ã DisplayName ã\n" + me.displayName)
                        elif cmd == 'à¸à¸±à¸ª':
                            me = client.getContact(to)
                            client.sendMessage(to,"ã StatusMessage ã\n" + me.statusMessage)
                        elif cmd == 'à¸à¸´à¸ª':
                            me = client.getContact(to)
                            client.sendImageWithURL(to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                        elif cmd == 'à¸§à¸µà¸à¸µà¹à¸­':
                            me = client.getContact(to)
                            client.sendVideoWithURL(to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                        elif cmd == 'memecode':
                            client.sendMessage(to,"10 Guy, tenguy\nAfraid to Ask Andy, afraid\nAn Older Code Sir, But It Checks Out, older\nAncient Aliens Guy, aag\nAt Least You Tried, tried\nBaby Insanity Wolf, biw\nBad Luck Brian, blb\nBut That's None of My Business, kermit\nButthurt Dweller, bd\nCaptain Hindsight, ch\nComic Book Guy, cbg\nCondescending Wonka, wonka\nConfession Bear, cb\nConspiracy Keanu, keanu\nDating Site Murderer, dsm\nDo It Live!, live\nDo You Want Ants?, ants\nDoge, doge\nDrake Always On Beat, alwaysonbeat\nErmahgerd, ermg\nFirst World Problems, fwp\nForever Alone, fa\nFoul Bachelor Frog, fbf\nFuck Me, Right?, fmr\nFuturama Fry, fry\nGood Guy Greg, ggg\nHipster Barista, hipster\nI Can Has Cheezburger?, icanhas\nI Feel Like I'm Taking Crazy Pills, crazypills\nI Immediately Regret This Decision!, regret\nI Should Buy a Boat Cat, boat\nI Would Be So Happy, sohappy\nI am the Captain Now, captain\nInigo Montoya, inigo\nInsanity Wolf, iw\nIt's A Trap!, ackbar\nIt's Happening, happening\nIt's Simple, Kill the Batman, joker\nJony Ive Redesigns Things, ive\nLaughing Lizard, ll\nMatrix Morpheus, morpheus\nMilk Was a Bad Choice, badchoice\nMinor Mistake Marvin, mmm\nNothing To Do Here, jetpack\nOh, Is That What We're Going to Do Today?, red\nOne Does Not Simply Walk into Mordor, mordor\nOprah You Get a Car, oprah\nOverlay Attached Girlfriend, oag\nPepperidge Farm Remembers, remembers\nPhilosoraptor, philosoraptor\nProbably Not a Good Idea, jw\nSad Barack Obama, sad-obama\nSad Bill Clinton, sad-clinton\nSad Frog / Feels Bad Man, sadfrog\nSad George Bush, sad-bush\nSad Joe Biden, sad-biden\nSad John Boehner, sad-boehner\nSarcastic Bear, sarcasticbear\nSchrute Facts, dwight\nScumbag Brain, sb\nScumbag Steve, ss\nSealed Fate, sf\nSee? Nobody Cares, dodgson\nShut Up and Take My Money!, money\nSo Hot Right Now, sohot\nSocially Awesome Awkward Penguin, awesome-awkward\nSocially Awesome Penguin, awesome\nSocially Awkward Awesome Penguin, awkward-awesome\nSocially Awkward Penguin, awkward\nStop Trying to Make Fetch Happen, fetch\nSuccess Kid, success\nSuper Cool Ski Instructor, ski\nThat Would Be Great, officespace\nThe Most Interesting Man in the World, interesting\nThe Rent Is Too Damn High, toohigh\nThis is Bull, Shark, bs\nWhy Not Both?, both\nWinter is coming, winter\nX all the Y, xy\nX, X Everywhere, buzz\nXzibit Yo Dawg, yodawg\nY U NO Guy, yuno\nY'all Got Any More of Them, yallgot\nYou Should Feel Bad, bad\nYou Sit on a Throne of Lies, elf\nYou Were the Chosen One!, chosen\n\nExample : Meme buzz|look that|khie is cool")     
                        elif cmd == 'à¸à¸':
                            if client != None:
                                path = client.getProfileCoverURL(to)
                                path = str(path)
                                if settings["server"] == "VPS":
                                    client.sendImageWithURL(to, str(path))
                                else:
                                    urllib.urlretrieve(path, "steal.jpg")
                                    client.sendImage(to, "steal.jpg")
                            else:
                                client.sendMessage(to, "Talk Exception")
                        elif cmd == 'à¸à¸¶à¸à¸«à¸¡à¸':
                            if client != None:
                                me = client.getContact(to)
                                path = client.getProfileCoverURL(to)
                                path = str(path)
                                if settings["server"] == "VPS":
                                    client.sendMessage(msg.to,"ã Display Name ã\n" + me.displayName)
                                    client.sendMessage(msg.to,"ã Status Message ã\n" + me.statusMessage)
                                    client.sendMessage(msg.to,"ã MID ã\n" +  to)
                                    client.sendMessage(to, text=None, contentMetadata={'mid': to}, contentType=13)
                                    client.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                                    client.sendImageWithURL(to, str(path))
                                    client.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                                else:
                                    client.sendMessage(msg.to,"ã Display Name ã\n" + me.displayName)
                                    client.sendMessage(msg.to,"ã Status Message ã\n" + me.statusMessage)
                                    client.sendMessage(msg.to,"ã MID ã\n" +  to)
                                    client.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                                    client.sendImageWithURL(to, str(path))
                            else:
                                client.sendMessage(to, "Talk Exception")
                        elif cmd == "announclear" or cmd == "announce clear":
                            announce = client.getChatRoomAnnouncements(to)
                            try:
                                for a in announce:
                                    client.removeChatRoomAnnouncement(to, a.announcementSeq)
                                client.sendMessage(to, "Success Clear Announce In Group "+str(client.getGroup(to).name))
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd == "fight" or cmd == "zzzzz":
                               group = client.getGroup(to)
                               try:
                                   members = [mem.mid for mem in group.members]
                                   mortal = [mem.mid for mem in group.members]
                               except:
                                   members = [mem.mid for mem in group.members]
                                   mortal = [mem.mid for mem in group.members]
                               s = random.choice(members)
                               t = random.choice(mortal)
                               sam = "Mortal Kombat has been initiated. "+client.getContact(s).displayName+" must fight..."+client.getContact(t).displayName+"! FIGHTO!"                                    
                               client.sendMessage(to,str(sam)) 
                        elif cmd == "nekopoi" or cmd == "zzzzz":
                               r = requests.get("http://nekopoi.faith/")
                               data = BeautifulSoup(r.content, 'html5lib')
                               ret_= "Latest Update\n"
                               for sam in data.findAll('div', attrs={'class':'eroinfo'}):
                                    ret_+="\n"+sam.find('h2').text+"\n"
                                    ret_+="http://nekopoi.faith"+sam.find('a')['href']+"\n"                                                                                       
                               client.sendMessage(to,ret_)
                        elif cmd == "à¹à¸à¸à¸£à¸­à¸à¸«à¸à¸±à¸" or cmd == "zzzzz":
                               result = requests.get("http://jadwalnonton.com/")
                               data = BeautifulSoup(result.content, 'html5lib')
                               hasil = "Ã£ÂÂ Cinema XX1 Ã£ÂÂ\nType : à¸£à¸­à¸à¸«à¸à¸±à¸à¹à¸à¹à¸£à¸à¸§à¸±à¸à¸à¸µà¹\n"
                               no = 1
                               for dzin in data.findAll('div', attrs={'class':'col-xs-6 moside'}):
                                   hasil += "\n\n{}. {}".format(str(no), str(dzin.find('h2').text))
                                   hasil += "\n     Link : {}".format(str(dzin.find('a')['href']))
                                   no = (no+1)
                               client.sendMessage(to, str(hasil))
                        elif cmd == "motivate" or cmd == "zzzzz":
                               r = requests.get("https://talaikis.com/api/quotes/random")
                               data=r.text
                               data=json.loads(data)                                                                   
                               client.sendMessage(to,str(data["quote"]))
#==============================================================================================================
                        elif cmd.startswith("announcecrash"):
                            Text = cmd.replace("announcecrash ","")
                            Logo = "http://dl.profile.line-cdn.net/" + client.getGroup(to).pictureStatus
                            stype = 1
                            announce = ChatRoomAnnouncementContents(displayFields=5,text=Text,link=None,thumbnail=Logo)
                            client.createChatRoomAnnouncement(to,stype,announce)
                            sendMention(receiver, sender, "ã Create Announce ã\nType : Lock\nâ¢", "\nSuccess Create Announce Lock "+str(Text)+" in Group : "+str(client.getGroup(to).name))
                        elif cmd.startswith("announcecam"):
                            a = cmd.replace("announcecam", "")
                            z = client.getGroup(to)
                            anu = client.getContact(sender)
                            c = ChatRoomAnnouncementContents()
                            c.displayFields = 5
                            c.text = a
                            c.link = "line://nv/camera"
                            c.thumbnail = "https://s9.postimg.cc/ukurx5kvj/camera.png"
                            try:
                                client.createChatRoomAnnouncement(to, 1, c)
                                client.sendMessage(to, "Succes announce")
                            except Exception as e:
                               client.sendMessage(to, str(e))
                        elif cmd.startswith("announallgroup"):
                            a = cmd.replace("announallgroup", "")
                            group = client.groups
                            z = client.getGroup(to)
                            b = ChatRoomAnnouncementContents()
                            b.displayFields = 5
                            b.text = a
                            b.link = "line://ti/p/{}".format(client.getUserTicket().id)
                            for groups in group:
                                anu = client.getGroup(groups)
                                b.thumbnail = "http://dl.profile.line-cdn.net/{}".format(anu.pictureStatus)
                                client.createChatRoomAnnouncement(groups, 1, b)
                            client.sendMessage(to, "Succes announce {} to all group".format(str(a)))
                        elif cmd.startswith("announcelink"):
                            a = cmd.replace("announcelink", "")
                            cond = a.split("|")
                            if len(cond) == 1:
                                link = "https://line.me/ti/p/~yukie2k18"
                            else:
                                link = cond[1]
                            z = client.getGroup(to)
                            anu = client.getContact(sender)
                            c = ChatRoomAnnouncementContents()
                            c.displayFields = 5
                            c.text = cond[0]
                            c.link = link
                            c.thumbnail = "http://dl.profile.line-cdn.net/{}".format(anu.pictureStatus)
                            try:
                                client.createChatRoomAnnouncement(to, 1, c)
                                client.sendMessage(to, "Succes announce link")
                            except Exception as e:
                               client.sendMessage(to, str(e))
                        elif cmd.startswith("abroadcast"):
                            a = cmd.replace("abroadcast", "")
                            cond = a.split("|")
                            if len(cond) == 1:
                                link = "https://line.me/ti/p/~yukie2k18"
                            else:
                                link = cond[1]
                            group = client.groups
                            b = ChatRoomAnnouncementContents()
                            b.displayFields = 5
                            b.text = cond[0]
                            b.link = link
                            for groups in group:
                                anu = client.getGroup(groups)
                                b.thumbnail = "http://dl.profile.line-cdn.net/{}".format(anu.pictureStatus)
                                client.createChatRoomAnnouncement(groups, 1, b)
                            client.sendMessage(to, "Succes announce link to all group")
                        elif cmd.startswith("à¹à¸­à¸à¸µ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                ret_ = ""
                                for ls in lists:
                                    ret_ += "{}".format(str(ls))
                                client.sendMessage(to, str(ret_))
                        elif cmd.startswith("gcastannoun "):
                            try:
                                message = cmd.replace("gcastannoun ","")
                                a = message.split("|")
                                Text = str(a[0])
                                Link = str(a[1])
                                Logo = "http://dl.profile.line-cdn.net/" + client.getContact(clientMID).pictureStatus
                                stype = 1
                                announce = ChatRoomAnnouncementContents(displayFields=5,text=Text,link=Link,thumbnail=Logo)
                                groups = client.getGroupIdsJoined()
                                for group in groups:
                                    client.createChatRoomAnnouncement(group,stype,announce)
                                client.sendMessage(to, "Success Broadcast Announce Lock {} to {} Groups".format(str(message), str(len(groups))))
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd.startswith("spam "):
                            dzin = cmd.replace("spam ","")
                            line = dzin.split("|")
                            count = int(line[1])
                            text1 = cmd.replace("spam "+str(line[0])+"|"+str(count)+"|","")
                            text2 = count * (text1+"\n")
                            if line[0] == "on":
                                if count <= 1000:
                                    for a in range(count):
                                        client.sendMessage(to, str(text1))
                                else:
                                    client.sendMessage(to, "Max 1000.")
                            if line[0] == "off":
                                if count <= 1000:
                                    client.sendMessage(to, str(text2))
                                else:
                                    client.sendMessage(to, "Max 1000.")
                        elif cmd.startswith("instagram "):
                               try:
                                   search = cmd.replace("instagram ","")
                                   r=requests.get("http://rahandiapi.herokuapp.com/instainfo/"+search+"?key=betakey")
                                   data = r.text
                                   data = json.loads(data)
                                   if data != []:
                                       ret_="Instagram Result:\n"
                                       ret_ += "\nName: {}".format(str(data["result"]["name"]))
                                       ret_ += "\nUsername: {}".format(str(data["result"]["username"]))                 
                                       ret_ += "\n\n {}".format(str(data["result"]["bio"]))            
                                       ret_ += "\n\nFollowers: {}".format(str(data["result"]["follower"]))
                                       ret_ += "\nFollowing: {}".format(str(data["result"]["following"]))                                 
                                       ret_ += "\nTotal Post: {}".format(str(data["result"]["mediacount"]))
                                       ret_ += "\nhttps://www.instagram.com/{}".format(search)
                                       path = data["result"]["url"]
                                       client.sendImageWithURL(to, str(path))
                                       client.sendMessage(to, str(ret_))
                               except Exception as error:
                                   logError(error)
                                   var= traceback.print_tb(error.__traceback__)
                                   client.sendMessage(to,str(var))
                        elif cmd.startswith("à¸à¸ "):
                            if client != None:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        me = client.getContact(ls)
                                    client.sendMessage(to, text=None, contentMetadata={'mid': ls}, contentType=13)
                        elif cmd.startswith("à¸à¸¶à¸à¸à¸·à¹à¸­ "):
                            if client != None:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        me = client.getContact(ls)
                                    client.sendMessage(msg.to,"ã à¸à¸·à¹à¸­ ã\n" + me.displayName)
                        elif cmd.startswith("à¸à¸·à¹à¸­ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    try:
                                	    rename = contact.displayNameOverridden
                                    except:
                                	    rename = "ã à¸à¸·à¹à¸­à¸à¸­à¸à¸à¸¸à¸ ã\nERROR"
                                    client.sendMessage(to, "ã à¸à¸·à¹à¸­à¸à¸­à¸à¸à¸¸à¸ ã\n" + contact.displayName + "\n\nã à¸à¸·à¹à¸­à¸à¸­à¸à¸à¸¸à¸ ã\n{}".format(rename))
                        elif cmd.startswith("à¸à¸±à¸ª "):
                            if client != None:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        me = client.getContact(ls)
                                    client.sendMessage(msg.to,"ã StatusMessage ã\n" + me.statusMessage)
                        elif cmd.startswith("à¸à¸´à¸ª "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = "http://dl.profile.line.naver.jp/" + client.getContact(ls).pictureStatus
                                    if settings["server"] == "VPS":
                                        client.sendImageWithURL(to, str(path))
                                    else:
                                        urllib.urlretrieve(path, "steal.jpg")
                                        client.sendImage(to, "steal.jpg")
                        elif cmd.startswith("à¸à¸ "):
                            if client != None:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        path = client.getProfileCoverURL(ls)
                                        path = str(path)
                                        if settings["server"] == "VPS":
                                            client.sendImageWithURL(to, str(path))
                                        else:
                                            urllib.urlretrieve(path, "steal.jpg")
                                            client.sendImage(to, "steal.jpg")
                            else:
                                client.sendMessage(to, "Tidak dapat masuk di line channel")
                        elif cmd.startswith("à¸§à¸µà¸à¸µà¹à¸­ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    path = "http://dl.profile.line-cdn.net/" + client.getContact(ls).pictureStatus + "/vp"
                                    if settings["server"] == "VPS":
                                        client.sendVideoWithURL(to, str(path))
                                    else:
                                        client.sendMessage(to, "User doesnt have profile Video ^_^")
                        elif cmd.startswith("à¹à¸à¸´à¹à¸¡à¹à¸à¸·à¹à¸­à¸ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    client.findAndAddContactsByMid(ls)
                                client.sendMessage(to, "à¹à¸à¸´à¹à¸¡à¸à¸¸à¸" + str(contact.displayName) + " à¹à¸à¹à¸à¹à¸à¸·à¹à¸­à¸à¹à¸¥à¹à¸§")
                        elif cmd.startswith("à¸à¸¥à¹à¸­à¸ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    client.blockContact(ls)
                                client.sendMessage(to, "à¸à¸¸à¸à¹à¸à¹à¸à¸³à¸à¸²à¸£à¸à¸¥à¹à¸­à¸ {} à¹à¸£à¸µà¸¢à¸à¸£à¹à¸­à¸¢à¹à¸¥à¹à¸§".format(str(contact.displayName)))
                        elif cmd.startswith("block:del "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    contact = client.getContact(ls)
                                    client.unblockContact(ls)
                                client.sendMessage(to, "Success Delete {} in Blocklist".format(str(contact.displayName)))
                        elif cmd.startswith("à¸à¸¶à¸à¸«à¸¡à¸ "):
                            if client != None:
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        me = client.getContact(ls)
                                        path = client.getProfileCoverURL(ls)
                                        path = str(path)
                                        if settings["server"] == "VPS":
                                            client.sendMessage(msg.to,"ã Display Name ã\n" + me.displayName)
                                            client.sendMessage(msg.to,"ã Status Message ã\n" + me.statusMessage)
                                            client.sendMessage(msg.to,"ã MID ã\n" +  to)
                                            client.sendMessage(to, text=None, contentMetadata={'mid': ls}, contentType=13)
                                            client.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                                            client.sendImageWithURL(to, str(path))
                                            client.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                                        else:
                                            client.sendMessage(msg.to,"ã Display Name ã\n" + me.displayName)
                                            client.sendMessage(msg.to,"ã Status Message ã\n" + me.statusMessage)
                                            client.sendMessage(msg.to,"ã MID ã\n" + ls)
                                            client.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                                            client.sendImageWithURL(to, str(path))
                                    else:
                                        client.sendMessage(to, "Talk Exception You are not Related to LineChannel")
                            else:
                                 client.sendMessage(to, "Talk Exception You are not Related to LineChannel")
                        elif cmd == "à¸£à¸¹à¸à¸«à¹à¸­à¸":
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                if settings["server"] == "VPS":
                                    client.sendImageWithURL(to, str(path))
                                else:
                                    urllib.urlretrieve(path, "gpict.jpg")
                                    client.sendImage(to, "gpict.jpg")
                        elif cmd.startswith("picgroup "):
                            saya = text.replace("picgroup ","")
                            gid = client.getGroupIdsJoined()
                            for i in gid:
                                h = client.getGroup(i).name
                                gna = client.getGroup(i)
                                if h == saya:
                                    path = ("http://dl.profile.line.naver.jp/"+ gna.pictureStatus)
                                    client.sendImageWithURL(to,path)
                        elif cmd.startswith("spic "):
                            saya = text.replace("spic ","")
                            gid = client.getAllContactIds()
                            for i in gid:
                                h = client.getContact(i).displayName
                                gna = client.getContact(i)
                                if h == saya:
                                    path = ("http://dl.profile.line.naver.jp/"+ gna.pictureStatus)
                                    client.sendImageWithURL(to,path)
#==============================================================================================================
                        elif cmd.startswith("clone:add "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    contact = mention["M"]
                                    break
                                try:
                                    client.cloneContactProfile(contact)
                                    client.sendMessage(msg.to, "Operation Succes!")
                                except:
                                    client.sendMessage(msg.to, "Operation Failure!")
                        elif cmd.startswith("cover:add "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    contact = mention["M"]
                                    break
                                try:
                                    client.CloneContactProfile(contact)
                                    client.sendMessage(msg.to, "Cloning cover Succes!")
                                except:
                                    client.sendMessage(msg.to, "Operation Failure!")
                        elif cmd == 'clone:del':
                                try:
                                    clientProfile.displayName = str(myProfile["displayName"])
                                    clientProfile.statusMessage = str(myProfile["statusMessage"])
                                    clientProfile.pictureStatus = str(myProfile["pictureStatus"])
                                    client.updateProfileAttribute(8, clientProfile.pictureStatus)
                                    client.updateProfile(clientProfile)
                                    client.sendMessage(msg.to, "Deleted Cloning Succses !")
                                except:
                                    client.sendMessage(msg.to, "Gagal restore profile failure!")
#==============================================================================================================
                        elif cmd.startswith("à¸£à¸±à¸à¸à¸¥à¸­ "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            cond = text.split(" ")
                            jml = int(cond[0])
                            if msg.toType == 2:
                                group = client.getGroup(to)
                            for x in range(jml):
                                members = [mem.mid for mem in group.members]
                                client.acquireGroupCallRoute(to)
                                client.inviteIntoGroupCall(to, contactIds=members)
                            else:
                                client.sendMessage(to, "à¸à¹à¸à¸à¸à¸±à¸à¹à¸«à¸à¸²à¸­à¸°".format(str(jml)))
                        elif cmd.startswith("à¸§à¹à¸² "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            cond = text.split(" ")
                            jml = int(cond[0])
                            if msg.toType == 2:
                                group = client.getGroup(to)
                            for x in range(jml):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for receiver in lists:
                                        contact = client.getContact(receiver)
                                        RhyN_(to, contact.mid)
                        elif cmd.startswith("à¹à¸«à¸à¸² "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            cond = text.split(" ")
                            jml = int(cond[0])
                            for x in range(jml):
                                name = client.getContact(to)
                                RhyN_(to, name.mid)
                        elif cmd == ".":
                            if msg.toType == 0:
                                sendMention(to, to, "", "")
                            elif msg.toType == 2:
                                group = client.getGroup(to)
                                contact = [mem.mid for mem in group.members]
                                mentionMembers(to, contact)
                        elif cmd.startswith("à¹à¸à¸ "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            cond = text.split(" ")
                            jml = int(cond[0])
                            if msg.toType == 2:
                                group = client.getGroup(to)
                            for x in range(jml):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for receiver in lists:
                                        client.sendMessage(receiver, text=None, contentMetadata=None, contentType=9)
                                        client.sendMessage(to, "à¸ªà¹à¸à¸à¸­à¸à¸à¸§à¸±à¸à¹à¸ à¸ª.à¸ à¹à¸¥à¹à¸§".format(str(jml)))
                                    else:
                                        pass
                        elif cmd.startswith("à¹à¸§à¸£à¸±à¸ª "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            cond = text.split(" ")
                            jml = int(cond[0])
                            if msg.toType == 2:
                                group = client.getGroup(to)
                            for x in range(jml):
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for receiver in lists:
                                        client.sendMessage(receiver, text=None, contentMetadata={'mid': "0',"}, contentType=13)
                                        client.sendMessage(to, "à¹à¸à¸à¸¹ à¸ª.à¸ à¸à¹à¸§à¸¢".format(str(jml)))
                                    else:
                                        pass
#==============================================================================================================
                        elif cmd.startswith("à¸à¸£à¸°à¸à¸²à¸¨ "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            groups = client.groups
                            for group in groups:
                                client.sendMessage(group, "ã à¸à¸£à¸°à¸à¸²à¸¨à¹ ã\n{}".format(str(txt)))
                            client.sendMessage(to, "à¸ªà¹à¸à¸à¹à¸­à¸à¸§à¸²à¸¡ à¸à¸°à¸à¸²à¸¨ à¸à¸±à¹à¸à¸«à¸¡à¸ {} à¸à¸¥à¸¸à¹à¸¡".format(str(len(groups))))
                        elif cmd.startswith("friendbcast "):
                            sep = text.split(" ")
                            txt = text.replace(sep[0] + " ","")
                            friends = client.friends
                            for friend in friends:
                                client.sendMessage(friend, "ã Broadcasted ã\n{}".format(str(txt)))
                            client.sendMessage(to, "Succes Broadcasted to {} Friends".format(str(len(friends))))
                        elif cmd.startswith("all bcast "):
                            try:
                                message = cmd.replace("all broadcast ","")
                                friends = client.friends
                                groups = client.groups
                                favorites = client.getFavoriteMids()
                                for friend in friends:
                                    client.sendMessage(friend, str(message))
                                client.sendMessage(to, "Success Broadcast {} to {} Friends".format(str(message), str(len(friends))))
                                for group in groups:
                                    client.sendMessage(group, str(message))
                                client.sendMessage(to, "Success Broadcast {} to {} Groups".format(str(message), str(len(groups))))
                                for favorite in favorites:
                                    client.sendMessage(favorite, str(message))
                                client.sendMessage(to, "Success Broadcast {} to {} Favorites".format(str(message), str(len(favorites))))
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
#==============================================================================================================
                        elif "/ti/g/" in msg.text.lower():
                            if settings["autoJoinTicket"] == True:
                                link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                                links = link_re.findall(text)
                                n_links = []
                                for l in links:
                                    if l not in n_links:
                                        n_links.append(l)
                                for ticket_id in n_links:
                                    group = client.findGroupByTicket(ticket_id)
                                    client.acceptGroupInvitationByTicket(group.id,ticket_id)
                                    client.sendMessage(to, "Succes join to group %s" % str(group.name))
#==============================================================================================================
                        elif cmd == "à¹à¸§à¸¥à¸²" or cmd == "kalender":
                            tz = pytz.timezone("Asia/Jakarta")
                            timeNow = datetime.datetime.now(tz=tz)
                            day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                            hari = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                            bulan = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                            hr = timeNow.strftime("%A")
                            bln = timeNow.strftime("%m")
                            for i in range(len(day)):
                                if hr == day[i]: hasil = hari[i]
                            for k in range(0, len(bulan)):
                                if bln == str(k): bln = bulan[k-1]
                            anu = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nà¹à¸§à¸¥à¸² : ã " + timeNow.strftime('%H:%M:%S') + " ã"
                            client.sendMessage(to, anu)
                        elif cmd == "à¸¥à¸à¹à¸à¸":
                            client.removeAllMessages(op.param2)
                            client.sendMessage(to, "à¸¥à¹à¸²à¸à¹à¸à¸à¸«à¸¡à¸à¹à¸¥à¹à¸§")
                        elif cmd == "à¹à¸à¸¥à¸°":
                            if msg.toType == 2:
                                client.leaveGroup(to)
                        elif cmd == "à¸à¸à¸ªà¸£à¹à¸²à¸à¸à¸¥à¸¸à¹à¸¡":
                            ginfo = client.getGroup(to)
                            gCreator = ginfo.creator.mid
                            try:
                                gCreator1 = ginfo.creator.displayName
                            except:
                                gCreator = "Not Found"
                            client.sendMessage(to, text=None, contentMetadata={'mid': gCreator}, contentType=13)
                            sendMention(to, gCreator, "à¸ªà¸§à¸±à¸ªà¸à¸µà¸à¸£à¸±à¸", "à¸à¸²à¸à¸à¸±à¸§à¸à¹à¸§à¸¢à¸à¸°à¸à¸£à¸±à¸à¹à¸­à¸")
                        elif cmd == "à¸à¸à¹à¸à¸à¸¥à¸¸à¹à¸¡":
                                kontak = client.getGroup(to)
                                group = kontak.members
                                num=1
                                msgs="ã à¸£à¸²à¸¢à¸à¸·à¹à¸­à¸à¸à¹à¸à¸à¸¥à¸¸à¹à¸¡ ã"
                                for ids in group:
                                    msgs+="\n%i. %s" % (num, ids.displayName)
                                    num=(num+1)
                                msgs+="\nà¸à¸³à¸à¸§à¸: %i à¸à¸" % len(group)
                                client.sendMessage(to, msgs)
                        elif cmd == 'à¸à¸¥à¹à¸­à¸':
                            blockedlist = client.getBlockedContactIds()
                            kontak = client.getContacts(blockedlist)
                            num=1
                            msgs="ã à¸à¸à¸à¸µà¹à¹à¸£à¸²à¸à¸¥à¹à¸­à¸ ã"
                            for ids in kontak:
                                msgs+="\n %i %s" % (num, ids.displayName)
                                num=(num+1)
                            msgs+="\nà¸à¸¸à¸à¹à¸à¹à¸à¸³à¸à¸²à¸£à¸à¸¥à¹à¸­à¸à¹à¸à¸·à¹à¸­à¸à¹à¸¥à¹à¸§ %i" % len(kontak)
                            client.sendMessage(msg.to, msgs)
                        elif cmd == "à¹à¸à¸à¸à¸³" or cmd == "banlist":
                            if settings["blacklist"] == []:
                                client.sendMessage(to,"ã à¸£à¸²à¸¢à¸à¸·à¹à¸­à¸à¸à¸à¸´à¸à¸à¸³ ã")
                            else:
                                num = 1
                                mc = "ã à¸£à¸²à¸¢à¸à¸·à¹à¸­à¸à¸à¸à¸´à¸à¸à¸³ ã"
                                for me in settings["blacklist"]:
                                    mc += "\n%i.  %s" % (num, client.getContact(me).displayName)
                                    num = (num+1)
                                mc += "\nãà¸à¸³à¸à¸§à¸ %i à¸à¸à¸à¸´à¸à¸à¸³ã" % len(settings["blacklist"])
                                client.sendMessage(to, mc)
                        elif cmd.startswith("à¸à¸±à¹à¸à¸à¸·à¹à¸­à¸à¸¥à¸¸à¹à¸¡ "):
                            sep = text.split(" ")
                            if msg.toType == 2:
                                try:
                                    group = client.getGroup(to)
                                    group.name = text.replace(sep[0] + " ","")
                                    client.updateGroup(group)
                                except:
                                    pass
                        elif cmd == "à¹à¸à¸´à¸à¸¥à¸´à¹à¸" or cmd == "ourl":
                            if msg.toType == 2:
                                g = client.getGroup(msg.to)
                                if g.preventedJoinByTicket == True:
                                    g.preventedJoinByTicket = False
                                    client.updateGroup(g)
                                gurl = client.reissueGroupTicket(msg.to)
                                client.sendMessage(msg.to,"ãà¸à¸¥à¸¸à¹à¸¡ã\n\n\nhttp://line.me/R/ti/g/" + gurl)
                        elif cmd == "à¸à¸´à¸à¸¥à¸´à¹à¸" or cmd == "close":
                            if msg.toType == 2:
                                group = client.getGroup(msg.to)
                                group.preventedJoinByTicket = True
                                client.updateGroup(group)
                        elif cmd == ".à¸à¸" or cmd == "mycon":
                            try:
                    	        sendMention(to, sender, "ã â¬à¸à¸·à¹à¸­ à¹à¸à¸¥à¸à¸­à¸â¬ ã\nâ¢", "")
                    	        client.sendContact(to, sender)
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))                              
#==============================================================================================================
                        elif cmd == "à¹à¸à¸´à¸à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸":
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                                bulan = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nà¹à¸§à¸¥à¸² : ã " + timeNow.strftime('%H:%M:%S') + " ã"
                                if msg.to in read['readPoint']:
                                        try:
                                            del read['readPoint'][msg.to]
                                            del read['readMember'][msg.to]
                                            del read['readTime'][msg.to]
                                        except:
                                            pass
                                        read['readPoint'][msg.to] = msg.id
                                        read['readMember'][msg.to] = ""
                                        read['readTime'][msg.to] = datetime.datetime.now().strftime('%H:%M:%S')
                                        read['ROM'][msg.to] = {}
                                        with open('sider.json', 'w') as fp:
                                            json.dump(read, fp, sort_keys=True, indent=4)
                                            client.sendMessage(msg.to,"Lurking already on")
                                else:
                                    try:
                                        del read['readPoint'][msg.to]
                                        del read['readMember'][msg.to]
                                        del read['readTime'][msg.to]
                                    except:
                                        pass
                                    read['readPoint'][msg.to] = msg.id
                                    read['readMember'][msg.to] = ""
                                    read['readTime'][msg.to] = datetime.datetime.now().strftime('%H:%M:%S')
                                    read['ROM'][msg.to] = {}
                                    with open('sider.json', 'w') as fp:
                                        json.dump(read, fp, sort_keys=True, indent=4)
                                        client.sendMessage(msg.to, "à¸à¸£à¸§à¸à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸:\n" + readTime)
                        elif cmd == "à¸à¸´à¸à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸":
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                                bulan = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nà¹à¸§à¸¥à¸² : ã " + timeNow.strftime('%H:%M:%S') + " ã"
                                if msg.to not in read['readPoint']:
                                    client.sendMessage(msg.to,"Lurking already off")
                                else:
                                    try:
                                            del read['readPoint'][msg.to]
                                            del read['readMember'][msg.to]
                                            del read['readTime'][msg.to]
                                    except:
                                          pass
                                    client.sendMessage(msg.to, "à¸à¸´à¸à¸à¸£à¸§à¸à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸:\n" + readTime)
                        elif cmd == 'à¸¥à¹à¸²à¸à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸':
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.datetime.now()
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                                bulan = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nà¹à¸§à¸¥à¸² : ã " + timeNow.strftime('%H:%M:%S') + " ã"
                                if msg.to in read["readPoint"]:
                                    try:
                                        read["readPoint"][msg.to] = True
                                        read["readMember"][msg.to] = {}
                                        read["readTime"][msg.to] = readTime
                                        read["ROM"][msg.to] = {}
                                    except:
                                        pass
                                    client.sendMessage(msg.to, "à¸¥à¹à¸²à¸à¸à¸£à¸§à¸à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸:\n" + readTime)
                                else:
                                    client.sendMessage(msg.to, "Lurking belum diaktifkan ngapain di reset?")
                        elif cmd == 'à¹à¸à¸à¸à¸à¸­à¹à¸²à¸':
                                tz = pytz.timezone("Asia/Jakarta")
                                timeNow = datetime.datetime.now()
                                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                                hari = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                                bulan = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]: hasil = hari[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k): bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nà¹à¸§à¸¥à¸² : ã " + timeNow.strftime('%H:%M:%S') + " ã"
                                if receiver in read['readPoint']:
                                    if read["ROM"][receiver].items() == []:
                                        client.sendMessage(receiver,"[ Reader ]:\nNone")
                                    else:
                                        chiya = []
                                        for rom in read["ROM"][receiver].items():
                                            chiya.append(rom[1])
                                        cmem = client.getContacts(chiya) 
                                        zx = ""
                                        zxc = ""
                                        zx2 = []
                                        xpesan = 'ã à¸à¸à¸­à¹à¸²à¸ ã\n'
                                    for x in range(len(cmem)):
                                        xname = str(cmem[x].displayName)
                                        pesan = ''
                                        pesan2 = pesan+"@c\n"
                                        xlen = str(len(zxc)+len(xpesan))
                                        xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                                        zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                                        zx2.append(zx)
                                        zxc += pesan2
                                    text = xpesan+ zxc + "\n" + readTime
                                    try:
                                        client.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                                    except Exception as error:
                                        print (error)
                                    pass
                                else:
                                    client.sendMessage(receiver,"à¹à¸£à¸´à¹à¸¡à¸à¸±à¸à¸à¸à¸­à¹à¸²à¸à¹à¸«à¸¡à¹")
#==============================================================================================================
                        elif cmd == "à¸à¸´à¸à¹à¸£à¸²" or cmd == " gift sticker 1":
                            a = int("1")
                            b = int("1000")
                            c = str("EN")
                            d = client.getActivePurchases(a, b, c, c)
                            ret_ = "ã à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¹à¸à¸­à¸à¹à¸£à¸² ã"
                            no =1
                            jmlh = []
                            for x in d.productList:
                                ret_ += "\n {}. {}".format(str(no), str(x.title))
                                no += 1
                                jmlh.append(x.title)
                            ret_ += "\nã à¸à¸³à¸à¸§à¸ {} à¸à¸±à¸§ ã".format(str(len(jmlh)))
                            client.sendMessage(to, str(ret_),contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+client.getContact(clientMID).pictureStatus, 'AGENT_NAME': 'MY STICKERS', 'AGENT_LINK': 'http://line.me/ti/p/~yukie2k18'})

                        elif cmd == "announclear" or cmd == " gift sticker 1":
                            a = client.getChatRoomAnnouncements(to)
                            client.sendMessage(to,"Announce cleared from group.")
                            try:
                             	for b in a:
                                     client.removeChatRoomAnnouncement(to,b.announcementSeq)                                     
                            except Exception as error:
                                logError(error)
                                traceback.print_tb(error.__traceback__)
                        elif cmd == "gift sticker 1" or cmd == " gift sticker 1":
                            client.sendGift(msg.to,'2351','sticker')
                        elif cmd == "gift" or cmd == " gift":
                                client.sendGift(msg.to,'1002077','sticker')
                        elif cmd == "à¹à¸à¸´à¸à¹à¸­à¸à¸­à¹à¸²à¸" or cmd == "cek sider:on":
                            try:
                                del sider['point'][receiver]
                                del sider['sidermem'][receiver]
                                del sider['cyduk'][receiver]
                            except:
                                pass
                            sider['point'][receiver] = msg.id
                            sider['sidermem'][receiver] = ""
                            sider['cyduk'][receiver]=True
                            client.sendMessage(receiver, "à¹à¸à¸´à¸à¹à¸à¸à¸à¸à¹à¸­à¸à¸­à¹à¸²à¸à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¹à¸­à¸à¸­à¹à¸²à¸" or cmd == "cek sider:off":
                            if msg.to in sider['point']:
                                sider['cyduk'][receiver]=False
                                client.sendMessage(receiver, sider['sidermem'][msg.to])
                            else:
                                client.sendMessage(receiver, "à¸à¸´à¸à¹à¸à¸à¸à¸à¹à¸­à¸à¸­à¹à¸²à¸à¹à¸¥à¹à¸§")
#==============================================================================================================
                        elif cmd == "à¸à¸±à¹à¸à¸à¹à¸²":
                            md = "âââ[ à¸à¸²à¸£à¸à¸±à¹à¸à¸à¹à¸²à¸à¸±à¹à¸à¸«à¸¡à¸ ]\n"
                            if settings["autoRead"] == True: md+="â  à¸­à¹à¸²à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸­à¹à¸²à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ ãà¸à¸´à¸ã\n"
                            if settings["mimic"]["status"] == True: md+="â  à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ãà¸à¸´à¸ã\n"
                            if settings["autoAdd"] == True: md+="â  à¸£à¸±à¸à¹à¸à¸·à¹à¸­à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸£à¸±à¸à¹à¸à¸·à¹à¸­à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ãà¸à¸´à¸ã\n"
                            if settings["autoBlock"] == True: md+="â  à¸­à¸­à¹à¸à¹à¸à¸¥à¹à¸­à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸­à¸­à¹à¸à¹à¸à¸¥à¹à¸­à¸ãà¸à¸´à¸ã\n"
                            if settings["autoLeave"] == True: md+="â  à¸­à¸­à¸à¹à¸à¸à¸£à¸§à¸¡ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸­à¸­à¸à¹à¸à¸à¸£à¸§à¸¡ãà¸à¸´à¸ã\n"
                            if settings["autoJoin"] == True: md+="â  à¹à¸à¹à¸²à¸à¸¥à¸¸à¹à¸¡à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¹à¸à¹à¸²à¸à¸¥à¸¸à¹à¸¡à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ãà¸à¸´à¸ã\n"
                            if settings["autoJoinTicket"] == True: md+="â  à¸¡à¸¸à¸à¸¥à¸´à¹à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸¡à¸¸à¸à¸¥à¸´à¹à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´ãà¸à¸´à¸ã\n"
                            if settings["checkContact"] == True: md+="â  à¸­à¹à¸²à¸à¸à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸­à¹à¸²à¸à¸à¸ãà¸à¸´à¸ã\n"
                            if settings["unsendMessage"] == True: md+="â  Resendchatãà¹à¸à¸´à¸ã\n"
                            else: md+="â  Resendchatãà¸à¸´à¸ã\n"
                            if settings["detectMention"] == True: md+="â  à¸à¸­à¸à¹à¸à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸à¸­à¸à¹à¸à¸ãà¸à¸´à¸ã\n"
                            if settings["detectMentionPM"] == True: md+="â  à¸à¸­à¸à¹à¸à¸ à¸ª.à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸à¸­à¸à¹à¸à¸ à¸ª.à¸ãà¸à¸´à¸ã\n"
                            if settings["welcomeMessage"] == True: md+="â  à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¹à¸­à¸à¸£à¸±à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¹à¸­à¸à¸£à¸±à¸ãà¸à¸´à¸ã\n"
                            if settings["leaveMessage"] == True: md+="â  à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¸­à¸ ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¸­à¸ãà¸à¸´à¸ã\n"
                            if settings["notag"] == True: md+="â  à¹à¸à¸à¹à¸à¸°ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¹à¸à¸à¹à¸à¸°ãà¸à¸´à¸ã\n"
                            if settings["autoReply"] == True: md+="â  Sleepmodeãà¹à¸à¸´à¸ã\n"
                            else: md+="â  Sleepmodeãà¸à¸´à¸ã\n"
                            if settings["sticker"] == True: md+="â  à¹à¸à¸°à¸à¸à¸¥à¸à¸à¸´à¹à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¹à¸à¸°à¸à¸à¸¥à¸à¸à¸´à¹à¸ãà¸à¸´à¸ã"
                            if settings["checkSticker"] == True: md+="â  à¹à¸à¹à¸à¸à¸´à¹à¸ãà¹à¸à¸´à¸ã\n"
                            else: md+="â  à¹à¸à¹à¸à¸à¸´à¹à¸ãà¸à¸´à¸ã"
                            #md = "\nâââ[ à¸à¸±à¹à¸à¸«à¸¡à¸ ]"
                            client.sendMessage(to,md+"")
                            
#====================
                        elif cmd == "à¹à¸à¸´à¸à¹à¸­à¸":
                            settings["autoAdd"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸£à¸±à¸à¹à¸à¸·à¹à¸­à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¹à¸­à¸":
                            settings["autoAdd"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸£à¸±à¸à¹à¸à¸·à¹à¸­à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´à¹à¸¥à¹à¸§")
#====================
                        elif cmd == "à¹à¸à¸´à¸à¸¡à¸¸à¸à¸¥à¸´à¹à¸":
                            settings["autoJoinTicket"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸¡à¸¸à¸à¸¥à¸´à¹à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´")
                        elif cmd == "à¸à¸´à¸à¸¡à¸¸à¸à¸¥à¸´à¹à¸":
                            settings["autoJoinTicket"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸¡à¸¸à¸à¸¥à¸´à¹à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´")
#====================
#====================
                        elif cmd == "detailuser on" or cmd == "à¹à¸à¸´à¸à¸à¸":
                            settings["checkContact"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸à¸²à¸£à¸­à¹à¸²à¸à¸à¸à¹à¸¥à¹à¸§")
                        elif cmd == "detailuser off" or cmd == "à¸à¸´à¸à¸à¸":
                            settings["checkContact"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸à¸²à¸£à¸­à¹à¸²à¸à¸à¸à¹à¸¥à¹à¸§")
#====================
                        elif cmd == "respongroupcall on":
                            settings["responGc"] = True
                            client.sendMessage(to, "Success activated Respon GroupCall")
                        elif cmd == "respongroupcall off":
                            settings["responGc"] = False
                            client.sendMessage(to, "Success deactived Respon GroupCall")
#====================
                        elif cmd == "à¹à¸à¸´à¸à¹à¸à¹à¸²":
                            settings["autoJoin"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¹à¸à¹à¸²à¸à¸¥à¸¸à¹à¸¡à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´")
                        elif cmd == "à¸à¸´à¸à¹à¸à¹à¸²":
                            settings["autoJoin"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¹à¸à¹à¸²à¸à¸¥à¸¸à¹à¸¡à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´")
#====================
                        elif cmd == "à¹à¸à¸´à¸à¸­à¸­à¸à¹à¸à¸":
                            settings["autoLeave"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸­à¸­à¸à¹à¸à¸à¸£à¸§à¸¡à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¸­à¸­à¸à¹à¸à¸":
                            settings["autoLeave"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸­à¸­à¸à¹à¸à¸à¸£à¸§à¸¡à¹à¸¥à¹à¸§")
#====================
                        elif cmd == "à¹à¸à¸´à¸à¸­à¹à¸²à¸":
                            settings["autoRead"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸à¸²à¸£à¸­à¹à¸²à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¸­à¹à¸²à¸":
                            settings["autoRead"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸à¸²à¸£à¸­à¹à¸²à¸à¸­à¸±à¸à¹à¸à¸¡à¸±à¸à¸´à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¹à¸à¹à¸à¸´à¸" or cmd == " sticker on":
                            settings["checkSticker"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸à¸²à¸£à¹à¸à¹à¸à¹à¸à¹à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¹à¸à¸à¸´à¸":
                            settings["checkSticker"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸à¸²à¸£à¹à¸à¹à¸à¹à¸à¹à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¹à¸¥à¹à¸§")
                        elif cmd == "resendchat on":
                            settings["unsendMessage"] = True
                            client.sendMessage(to, "Resend message has been enabled")
                        elif cmd == "resendchat off":
                            settings["unsendMessage"] = False
                            client.sendMessage(to, "Resend message has been disabled")
                        elif cmd == "à¹à¸à¸´à¸à¸à¸¥à¹à¸­à¸":
                            settings["autoBlock"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸­à¸­à¹à¸à¹à¸à¸¥à¹à¸­à¸à¸ªà¸³à¹à¸£à¹à¸à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¸à¸¥à¹à¸­à¸":
                            settings["autoBlock"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸­à¸­à¹à¸à¹à¸à¸¥à¹à¸­à¸à¸ªà¸³à¹à¸£à¹à¸à¸¥à¹à¸§")
                        elif cmd == "à¹à¸à¸´à¸à¹à¸à¸à¹à¸à¸°":
                            settings["notag"] = True
                            client.sendMessage(to, "à¹à¸à¸£à¹à¸à¸à¸¡à¸µà¸à¸¸à¸555")
                        elif cmd == "à¸à¸´à¸à¹à¸à¸à¹à¸à¸°":
                            settings["notag"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¹à¸à¸à¹à¸à¸°à¹à¸¥à¹à¸§")
                        elif cmd == "à¹à¸à¸´à¸à¸à¸à¸­à¸­à¸":
                            settings["leaveMessage"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¸­à¸à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¸à¸à¸­à¸­à¸":
                            settings["leaveMessage"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¸­à¸à¹à¸¥à¹à¸§")
                        elif cmd == "à¹à¸à¸´à¸à¸à¸à¹à¸à¹à¸²":
                            settings["welcomeMessage"] = True
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¹à¸à¹à¸²à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¸à¸à¹à¸à¹à¸²":
                            settings["welcomeMessage"] = False
                            client.sendMessage(to, "à¸à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¹à¸à¹à¸²à¹à¸¥à¹à¸§")
                        elif cmd == "sleepmode on":
                            settings["autoReply"] = True
                            client.sendMessage(to, "Success activated Sleep Mode")
                        elif cmd == "sleepmode off":
                            settings["autoReply"] = False
                            client.sendMessage(to, "Success deactived Sleep Mode")
                        elif cmd == "à¹à¸à¸´à¸à¹à¸­à¸":
                            settings["getReader"][receiver] = []
                            client.sendMessage(to, "à¹à¸à¸´à¸à¸à¸²à¸£à¸à¸£à¸§à¸à¸à¸±à¸à¸à¸à¹à¸­à¸à¸­à¹à¸²à¸")
                        elif cmd == "autocancel on":
                            settings["botcancel"] = True
                            client.sendMessage(to, "AutoRead has been enabled")
                        elif cmd == "autocancel off":
                            settings["botcancel"] = False
                            client.sendMessage(to, "AutoRead has been disabled")
                        elif cmd == "à¸à¸´à¸à¹à¸­à¸":
                            if receiver in settings["getReader"]:
                                del settings["getReader"][receiver]
                                client.sendMessage(to, "à¹à¸à¸´à¸à¸à¸²à¸£à¸à¸£à¸§à¸à¸à¸±à¸à¸à¸à¹à¸­à¸à¸­à¹à¸²à¸")
                        elif cmd == "à¹à¸à¸´à¸à¹à¸à¸°à¸à¸à¸¥à¸à¸à¸´à¹à¸" or cmd == "/nosticker:0":
                                settings["sticker"] = True
                                client.sendMessage(to,"à¹à¸à¸´à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¹à¸¥à¹à¸§")
                        elif cmd == "à¸à¸´à¸à¹à¸à¸°à¸à¸à¸¥à¸à¸à¸´à¹à¸" or cmd == "/nosticker:1":
                                settings["sticker"] = False
                                client.sendMessage(to,"à¸à¸´à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¹à¸¥à¹à¸§")
                        elif cmd == "sleepmode":
                            if settings["replyPesan"] is not None:
                                client.sendMessage(to,"Your Sleepmode is : " + str(settings["replyPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["sleepSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Sleepmode : No messages are set")
                        elif cmd == "addsleepmodesticker":
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "sleepSticker"
                            client.sendMessage(to, "please send a sticker if you want to add")
                        elif cmd == "delsleepmodesticker":
                            settings["messageSticker"]["listSticker"]["sleepSticker"] = None
                            client.sendMessage(to, "Success delete sticker")
                        elif cmd.startswith("setsleepmode: "):
                            text_ = cmd.replace("setsleepmode:", "")
                            try:
                                settings["replyPesan"] = text_
                                client.sendMessage(to,"Sleep mode changed to : " + text_)
                            except:
                                client.sendMessage(to,"SleepMode \nFailed to replace message")
                        elif cmd == "leavemessage":
                            if settings["leavePesan"] is not None:
                                client.sendMessage(to,"Your Leavemessage is : " + str(settings["leavePesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["leaveSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My LeaveMessage : No messages are set")
                        elif cmd == "à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¸­à¸­à¸":
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "leaveSticker"
                            client.sendMessage(to, "à¸ªà¹à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸µà¹à¸à¸°à¸à¸±à¹à¸à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸¥à¸à¸à¸´à¹à¸à¸à¸à¸­à¸­à¸":
                            settings["messageSticker"]["listSticker"]["leaveSticker"] = None
                            client.sendMessage(to, "à¸¥à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸à¹à¸à¹à¸²à¹à¸¥à¹à¸§")
                        elif cmd.startswith("à¸à¸±à¹à¸à¸à¸à¸­à¸­à¸: "):
                            text_ = cmd.replace("à¸à¸±à¹à¸à¸à¸à¸­à¸­à¸:", "")
                            try:
                                settings["leavePesan"] = text_
                                client.sendMessage(to,"à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¸­à¸­à¸à¸«à¹à¸­à¸à¸à¸­à¸à¸à¸¸à¸ : " + text_)
                            except:
                                client.sendMessage(to,"LeaveMessage\nFailed to replace message")
                        elif cmd == "welcomemessage":
                            if settings["welcomePesan"] is not None:
                                client.sendMessage(to,"Your Welcomemessage is : " + str(settings["welcomePesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["welcomeSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set WelcomeMessage : No messages are set")
                        elif cmd == "à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¹à¸²":
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "welcomeSticker"
                            client.sendMessage(to, "à¸ªà¹à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸µà¹à¸à¸°à¸à¸±à¹à¸à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¹à¸²":
                            settings["messageSticker"]["listSticker"]["welcomeSticker"] = None
                            client.sendMessage(to, "à¸¥à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸à¹à¸à¹à¸²à¹à¸¥à¹à¸§")
                        elif cmd.startswith("à¸à¸±à¹à¸à¸à¸à¹à¸à¹à¸²: "):
                            text_ = cmd.replace("à¸à¸±à¹à¸à¸à¸à¹à¸à¹à¸²:", "")
                            try:
                                settings["welcomePesan"] = text_
                                client.sendMessage(to,"à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸­à¸à¹à¸£à¸²à¸à¸­à¸à¸à¸¸à¸ : " + text_)
                            except:
                                client.sendMessage(to,"WelcomeMessage\nFailed to replace message")
                        elif cmd == "à¹à¸à¸":
                            if msg.toType == 0:
                                sendMention(to, to)
                            elif msg.toType == 2:
                                group = client.getGroup(to)
                                contact = [mem.mid for mem in group.members]
                                ct1, ct2, ct3, ct4, ct5, jml = [], [], [], [], [], len(contact)
                                if jml <= 100:
                                    mentionMembers(to, contact)
                                elif jml > 100 and jml <= 200:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, jml):
                                        ct2 += [contact[b]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                elif jml > 200 and jml <= 300:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, 199):
                                        ct2 += [contact[b]]
                                    for c in range(200, jml):
                                        ct3 += [contact[c]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                elif jml > 300 and jml <= 400:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, 199):
                                        ct2 += [contact[b]]
                                    for c in range(200, 299):
                                        ct3 += [contact[c]]
                                    for d in range(300, jml):
                                        ct4 += [contact[d]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                elif jml > 400 and jml <= 500:
                                    for a in range(0, 99):
                                        ct1 += [contact[a]]
                                    for b in range(100, 199):
                                        ct2 += [contact[b]]
                                    for c in range(200, 299):
                                        ct3 += [contact[c]]
                                    for d in range(300, 399):
                                        ct4 += [contact[d]]
                                    for e in range(400, jml):
                                        ct4 += [contact[e]]
                                    mentionMembers(to, ct1)
                                    mentionMembers(to, ct2)
                                    mentionMembers(to, ct3)
                                    mentionMembers(to, ct4)
                                    mentionMembers(to, ct5)
                        elif cmd == "autoadd":
                            if settings["addPesan"] is not None:
                                client.sendMessage(to,"Your Autoadd is : " + str(settings["addPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["addSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"My Set AutoAdd : No messages are set")
                        elif cmd == "à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸":
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "addSticker"
                            client.sendMessage(to, "à¸ªà¹à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸µà¹à¸à¸°à¹à¸à¹à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸":
                            settings["messageSticker"]["listSticker"]["addSticker"] = None
                            client.sendMessage(to, "à¸¥à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                        elif cmd.startswith("à¸à¸±à¹à¸à¸à¸à¹à¸­à¸: "):
                            text_ = cmd.replace("à¸à¸±à¹à¸à¸à¸à¹à¸­à¸:", "")
                            try:
                                settings["addPesan"] = text_
                                client.sendMessage(to,"à¸à¸³à¸à¸­à¸à¸à¸¥à¸±à¸à¸à¸à¹à¸­à¸à¸à¸­à¸à¸à¸¸à¸ : " + text_)
                            except:
                                client.sendMessage(to,"AutoAdd\nFailed to replace message")
                        elif cmd == "autorespon":
                            if settings["mentionPesan"] is not None:
                                client.sendMessage(to,"Your autorespon is : " + str(settings["mentionPesan"]))
                                msgSticker = settings["messageSticker"]["listSticker"]["responSticker"]
                                if msgSticker != None:
                                    sid = msgSticker["STKID"]
                                    spkg = msgSticker["STKPKGID"]
                                    sver = msgSticker["STKVER"]
                                    sendSticker(to, sver, spkg, sid)
                            else:
                                client.sendMessage(to,"Your Autorespon is : No messages are set")
                        elif cmd == "à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¸":
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "responSticker"
                            client.sendMessage(to, "à¸ªà¹à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸µà¹à¸à¸°à¹à¸à¹à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸à¸":
                            settings["messageSticker"]["listSticker"]["responSticker"] = None
                            client.sendMessage(to, "à¸¥à¸à¸ªà¸à¸´à¸à¹à¸à¸­à¸£à¸à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                        elif cmd.startswith("à¸à¸±à¹à¸à¹à¸à¸: "):
                            text_ = cmd.replace("à¸à¸±à¹à¸à¹à¸à¸:", "")
                            try:
                                settings["mentionPesan"] = text_
                                client.sendMessage(to,"à¸à¸³à¹à¸à¸ à¸à¸·à¸­ : " + text_)
                            except:
                                client.sendMessage(to,"à¸à¸³à¹à¸à¸ à¸à¸·à¸­")
                        elif cmd == "à¸à¸±à¹à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸":
                            settings["messageSticker"]["addStatus"] = True
                            settings["messageSticker"]["addName"] = "readerSticker"
                            client.sendMessage(to, "à¸ªà¹à¸à¸ªà¸à¸´à¹à¸à¹à¸à¸­à¸£à¸à¸µà¹à¸à¸°à¹à¸à¹à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸¥à¸à¸à¸´à¹à¸à¸à¸à¹à¸­à¸":
                            settings["messageSticker"]["listSticker"]["readerSticker"] = None
                            client.sendMessage(to, "à¸¥à¸à¸ªà¸à¸´à¹à¸à¹à¸à¸­à¸£à¸à¸à¹à¸­à¸à¸­à¹à¸²à¸à¹à¸¥à¹à¸§")
                        elif cmd.startswith("à¸à¸±à¹à¸à¸à¸à¹à¸­à¸: "):
                            text_ = cmd.replace("à¸à¸±à¹à¸à¸à¸à¹à¸­à¸:", "")
                            try:
                                settings["readerPesan"] = text_
                                client.sendMessage(to,"à¸à¸±à¹à¸à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸à¹à¸­à¸à¸­à¹à¸²à¸à¹à¸¥à¹à¸§ : " + text_)
                            except:
                                client.sendMessage(to,"à¸à¸³à¸¥à¸±à¸à¸à¸±à¹à¸\nà¸à¸±à¹à¸à¸ªà¸à¸´à¹à¸à¹à¸à¸­à¸£à¸à¸à¹à¸­à¸à¹à¸£à¸µà¸¢à¸à¸£à¹à¸­à¸¢")
#==============================================================================================================
                        elif "à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ " in msg.text.lower():
                            mic = msg.text.lower().replace("à¹à¸¥à¸·à¸¢à¸à¹à¸à¸ ","")
                            if mic == "à¹à¸à¸´à¸":
                                if settings["mimic"]["status"] == False:
                                    settings["mimic"]["status"] = True
                                    client.sendMessage(msg.to,"à¹à¸à¸´à¸à¸à¸²à¸£à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                                else:
                                    client.sendMessage(msg.to,"à¹à¸à¸´à¸à¸à¸²à¸£à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                            elif mic == "à¸à¸´à¸":
                                if settings["mimic"]["status"] == True:
                                    settings["mimic"]["status"] = False
                                    client.sendMessage(msg.to,"à¸à¸´à¸à¸à¸²à¸£à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                                else:
                                    client.sendMessage(msg.to,"à¸à¸´à¸à¸à¸²à¸£à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
#==============================================================================#
                        elif msg.text.lower().startswith("à¹à¸¥à¸µà¸¢à¸à¹à¸à¸ "):
                            targets = []
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                try:
                                    settings["mimic"]["target"][target] = True
                                    client.sendMessage(msg.to,"à¸à¸±à¹à¸à¸à¸à¸à¸µà¹à¹à¸£à¸²à¸à¸°à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                                    break
                                except:
                                    client.sendMessage(msg.to,"à¸à¸±à¹à¸à¸à¸à¸à¸µà¹à¹à¸£à¸²à¸à¸°à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                                    break
                        elif msg.text.lower().startswith("à¸¥à¹à¸²à¸à¹à¸¥à¸µà¸¢à¸à¹à¸à¸ "):
                            targets = []
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                try:
                                    del settings["mimic"]["target"][target]
                                    client.sendMessage(msg.to,"à¸¥à¹à¸²à¸à¸à¸à¸à¸µà¹à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                                    break
                                except:
                                    client.sendMessage(msg.to,"à¸¥à¹à¸²à¸à¸à¸à¸à¸µà¹à¹à¸¥à¸µà¸¢à¸à¹à¸à¸à¹à¸¥à¹à¸§")
                                    break
                        elif text.lower() == 'à¹à¸à¸à¹à¸¥à¸µà¸¢à¸à¹à¸à¸':
                            if settings["mimic"]["target"] == {}:
                                client.sendMessage(msg.to,"Target in Mimic List Noneâª")
                            else:
                                num = 1
                                mc = "ã MimicList ã"
                                for mi_d in settings["mimic"]["target"]:
                                    mc += "\n â¢ "+client.getContact(mi_d).displayName
                                mc += "\nã Finish ã"
                                client.sendMessage(msg.to,mc)                     
                                
                        elif cmd.startswith("à¹à¸à¸«à¸³ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    try:
                                        client.kickoutFromGroup(to, [ls])
                                        client.inviteIntoGroup(to, [ls])
                                        client.cancelGroupInvitation(to, [ls])
                                    except:
                                       client.sendMessage(to, "Limited !")
                        elif cmd.startswith("à¸¥à¸­à¸à¸à¸¹ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    try:
                                        client.kickoutFromGroup(to, [ls])
                                        client.inviteIntoGroup(to, [ls])
                                        client.cancelGroupInvitation(to, [ls])
                                        time.sleep(5)
                                        client.inviteIntoGroup(to, [ls])
                                    except:
                                       client.sendMessage(to, "Limited !")
                        elif cmd.startswith("à¸¥à¹à¸­à¹à¸¥à¹à¸ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    try:
                                        client.kickoutFromGroup(to, [ls])
                                        time.sleep(5)
                                        client.inviteIntoGroup(to, [ls])
                                    except:
                                       client.sendMessage(to, "Limited !")

                        elif cmd.startswith("à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡ "):
                            wban = cmd.split()[1:]
                            wban = " ".join(wban)
                            wbanlist.append(wban)
                            client.sendMessage(to,"%s à¸à¸´à¸¡à¸à¸³à¸à¸µà¹à¸­à¸²à¸à¸¡à¸µà¸à¸¥à¸´à¸§à¸à¸°."%wban)
                        elif cmd.startswith("à¸¥à¹à¸²à¸à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡ "):
                            wunban = cmd.split()[1:]
                            wunban = " ".join(wunban)
                            if wunban in wbanlist:
                                wbanlist.remove(wunban)
                                client.sendMessage(to,"%s à¸¥à¹à¸²à¸à¸­à¸­à¸à¸à¸²à¸à¸à¸³à¸ªà¸±à¹à¸à¸«à¹à¸²à¸¡à¸à¸´à¸¡à¹à¸¥à¹à¸§."%wunban)
                            else:
                                client.sendMessage(to,"%s is not blacklisted."%wunban)
                        elif cmd == 'à¹à¸à¸à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡':
                            tst = "à¸à¸³à¸«à¹à¸²à¸¡à¸à¸´à¸¡:\n"
                            if len(wbanlist) > 0:
                                for word in wbanlist:
                                    tst += "- %s"%word
                                client.sendMessage(msg.to,tst)
                            else:
                                client.sendMessage(msg.to,"à¸à¸³à¸à¸µà¹à¸«à¹à¸²à¸¡à¸à¸´à¸¡à¸à¸±à¹à¸à¸«à¸¡à¸")
#==============================================================================================================
                        elif cmd.startswith("checkdate "):
                            tanggal = text.replace("checkdate ","")
                            r=requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                            data=r.text
                            data=json.loads(data)
                            ret_ = "ã D A T E \n"
                            ret_ += "\nãDate Of Birth : {}".format(str(data["data"]["lahir"]))
                            ret_ += "\nãAge : {}".format(str(data["data"]["usia"]))
                            ret_ += "\nãBirthday : {}".format(str(data["data"]["ultah"]))
                            ret_ += "\nãZodiak : {}".format(str(data["data"]["zodiak"]))
                            ret_ += "\n"
                            client.sendMessage(to, str(ret_))
                        elif cmd.startswith("wikipedia "):
                                try:
                                    sep = msg.text.split(" ")
                                    wiki = msg.text.replace(sep[0] + " ","")
                                    wikipedia.set_lang("id")
                                    pesan="ãTitle : "
                                    pesan+=wikipedia.page(wiki).title
                                    pesan+=" ã\nãIsi : "
                                    pesan+=wikipedia.summary(wiki, sentences=1)
                                    pesan+=" ã\nãLink : "+wikipedia.page(wiki).url
                                    pesan+=" ã\n"
                                    client.sendMessage(to, pesan)
                                except:
                                        try:
                                            pesan="Over Text Limit! Please Click link\n"
                                            pesan+=wikipedia.page(wiki).url
                                            client.sendMessage(to, pesan)
                                        except Exception as e:
                                            client.sendMessage(to, str(e))
                        elif cmd.startswith("music "):
                            sep = text.lower().split(" ")
                            query = text.lower().replace(sep[0] + " ","")
                            cond = query.split("|")
                            search = str(cond[0])
                            with requests.session() as web:
                                web.headers["user-agent"] = random.choice(settings["userAgent"])
                                result = web.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
                                data = result.text
                                data = json.loads(data)
                                if len(cond)  == 1:
                                    num = 0
                                    ret_ = "ã Music Search Results ã\nSearch : {}\n".format(str(query))
                                    for music in data["result"]:
                                        num += 1
                                        ret_ += "\n{}. Title : {}".format(str(num), str(music["single"]))
                                        ret_ += "\nArtist : {}".format(str(music["artist"]))
                                        ret_ += "\nAlbum : {}".format(str(music["album"]))
                                        ret_ += "\nPlayed : {}".format(str(music["played"]))
                                    ret_2 = "\n\nTotal {} Music".format(str(len(data["result"])))
                                    ret_3 = "\n\nUsage : Music {}|number".format(settings["keyCommand"],query)
                                    client.sendMessage(msg.to, str(ret_) + str(ret_2) + str(ret_3))
                                elif len(cond) == 2:
                                    num = int(cond[1])
                                    if num <= len(data["result"]):
                                        music = data["result"][num - 1]
                                        with requests.session() as web:
                                            web.headers["user-agent"] = random.choice(settings["userAgent"])
                                            result = web.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
                                            data = result.text
                                            data = json.loads(data)
                                            if data["result"] != []:
                                                ret_ = "ã Info Music {} ã\n".format(str(data["result"]["song"]))
                                                ret_ += "\nTitle : {}".format(str(data["result"]["song"]))
                                                ret_ += "\nAlbum : {}".format(str(data["result"]["album"]))
                                                ret_ += "\nSize : {}".format(str(data["result"]["size"]))
                                                ret_ += "\nLink : {}".format(str(data["result"]["mp3"][0]))
                                                client.sendImageWithURL(msg.to, str(data["result"]["img"]))
                                                client.sendMessage(msg.to, str(ret_))
                                                client.sendAudioWithURL(msg.to, str(data["result"]["mp3"][0]))
                        elif cmd.startswith("à¹à¸à¸µà¸¢à¸ "):
                                sep = msg.text.split(" ")
                                textnya = msg.text.replace(sep[0] + " ","")
                                path = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                                client.sendImageWithURL(msg.to,path)
                        elif cmd.startswith("video "):
                            try:
                                sep = msg.text.split(" ")
                                textToSearch = msg.text.replace(sep[0] + " ","")
                                query = urllib.parse.quote(textToSearch)
                                url = "https://www.youtube.com/results?search_query=" + query
                                response = urllib.request.urlopen(url)
                                html = response.read()
                                soup = BeautifulSoup(html, "html.parser")
                                results = soup.find(attrs={'class':'yt-uix-tile-link'})
                                dl=("https://www.youtube.com" + results['href'])
                                vid = pafy.new(dl)
                                stream = vid.streams
                                for s in stream:
                                    vin = s.url
                                    hasil = "ã Youtube - Video ã"
                                    hasil += "\nTitle : {}".format(str(vid.title))
                                    hasil += "\nSubscriber From : {}".format(str(vid.author))
                                    hasil += "\nPlease wait for the videos"
                                    hasil += "\n"
                                client.sendMessage(msg.to,hasil)
                                client.sendVideoWithURL(msg.to,vin)
                                print("[YOUTUBE]MP4 Succes")
                            except Exception as e:
                                client.sendMessage(to, str(e))
#==============================================================================================================
                        elif cmd.startswith("à¹à¸à¸´à¹à¸¡à¸à¸³ "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                        names = re.findall(r'@(\w+)', text)
                                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                        mentionees = mention['MENTIONEES']
                                        lists = []
                                        for mention in mentionees:
                                            if mention["M"] not in lists:
                                                lists.append(mention["M"])
                                        for target in lists:
                                            try:
                                                settings["blacklist"][target] = True
                                                del settings["whitelist"][target]
                                                f=codecs.open('st2__b.json','w','utf-8')
                                                json.dump(settings["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                                client.sendMessage(to,"")
                                                print("[Command] Bannad")
                                            except:
                                                pass
                        elif cmd.startswith("à¸¥à¸à¸à¸³ "):
                            sep = text.split(" ")
                            text = text.replace(sep[0] + " ","")
                            if msg.toType == 2:
                                group = client.getGroup(to)
                                if 'MENTION' in msg.contentMetadata.keys()!= None:
                                        names = re.findall(r'@(\w+)', text)
                                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                        mentionees = mention['MENTIONEES']
                                        lists = []
                                        for mention in mentionees:
                                            if mention["M"] not in lists:
                                                lists.append(mention["M"])
                                        for target in lists:
                                            try:
                                                del settings["blacklist"][target]
                                                f=codecs.open('st2__b.json','w','utf-8')
                                                json.dump(settings["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                                client.sendMessage(to,"")
                                                print("[Command] Bannad")
                                            except:
                                                pass
                        elif cmd == "à¸à¸³":
                            settings["wblacklist"] = True
                            client.sendMessage(to,"à¸ªà¹à¸ à¸à¸ à¸à¸à¸à¸µà¹à¸à¸¸à¸à¸à¸°à¸¢à¸±à¸à¸à¸³à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸à¸¥à¸à¸à¸³":
                            settings["dblacklist"] = True
                            client.sendMessage(to,"à¸ªà¹à¸ à¸à¸ à¸à¸à¸à¸µà¹à¸à¸¸à¸à¸¥à¹à¸²à¸à¸à¸³à¸¥à¸à¸¡à¸²")
                        elif cmd == "à¸à¸à¸à¸³" or cmd == "mute contact":
                            if msg._from in clientMID:
                                if settings["blacklist"] == []:
                                    client.sendMessage(to, "Nothing boss")
                                else:
                                    for bl in settings["blacklist"]:
                                        client.sendMessage(to, text=None, contentMetadata={'mid': bl}, contentType=13)
                        elif cmd == "à¸¥à¹à¸²à¸à¸à¸³":
                            settings["blacklist"] = {}
                            client.sendMessage(to,"ãà¸¥à¹à¸²à¸à¸à¸à¸à¸´à¸à¸à¸³à¸«à¸¡à¸à¹à¸£à¸µà¸¢à¸à¸£à¹à¸­à¸¢ã")
                        elif cmd.startswith("à¸¥à¸à¹à¸à¸·à¹à¸­à¸ "):
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    client.deleteContact(ls)
                                client.sendMessage(to, "à¸¥à¸à¸­à¸­à¸à¸à¸²à¸à¸à¸²à¸£à¹à¸à¹à¸à¹à¸à¸·à¹à¸­à¸à¹à¸¥à¹à¸§")
                        elif cmd == "motivation":
                             try:                                                                           
                                 r = requests.get("https://ari-api.herokuapp.com/images?q=quotes")
                                 data = r.text
                                 data = json.loads(data)
                                 if data["result"] != []:
                                     items = data["result"]
                                     path = random.choice(items)
                                     a = items.index(path)
                                     b = len(items)                                            
                                     client.sendImageWithURL(to, str(path))                                                   
                                     log.info("Image #%s from #%s." %(str(a),str(b)))
                             except Exception as error:
                                  log.info(error)
                        elif cmd == "conban":
                            if msg._from in clientMID:
                                blockedlist = client.getBlockedContactIds()
                                if blockedlist == []:
                                    client.sendMessage(to, "Gada yg di BLOCK!")
                                else:
                                    for kontak in blockedlist:
                                        client.sendMessage(to, text=None, contentMetadata={'mid': kontak}, contentType=13)
#==============================================================================================================
                        elif cmd == "แทค" or cmd == "tagall" or cmd == "desah" or cmd == "jembot":
                            group = client.getGroup(msg.to)
                            nama = [contact.mid for contact in group.members]
                            k = len(nama)//20
                            for a in range(k+1):
                                txt = u''
                                s=0
                                b=[]
                                for i in group.members[a*20 : (a+1)*20]:
                                    b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                                    s += 7
                                    txt += u'@RhyN_\n'
                                client.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
#==============================================================================================================
#==============================================================================================================
                        elif cmd.startswith("à¸à¸­à¸£à¸¹à¸ "):
                            try:
                                search = cmd.replace("à¸à¸­à¸£à¸¹à¸ ","")
                                r = requests.get("https://xeonwz.herokuapp.com/images/google.api?q={}".format(search))
                                data = r.text
                                data = json.loads(data)
                                if data["content"] != []:
                                    items = data["content"]
                                    path = random.choice(items)
                                    a = items.index(path)
                                    b = len(items)
                                    client.sendImageWithURL(to, str(path))
                            except Exception as error:
                                 logError(error)
                                 var= traceback.print_tb(error.__traceback__)
                                 client.sendMessage(to,str(var))
#==============================================================================================================
                        elif cmd.startswith("devianart "):
                            try:
                                search = cmd.replace("devianart ","")
                                r = requests.get("https://xeonwz.herokuapp.com/images/deviantart.api?q={}".format(search))
                                data = r.text
                                data = json.loads(data)
                                if data["content"] != []:
                                    items = data["content"]
                                    path = random.choice(items)
                                    a = items.index(path)
                                    b = len(items)
                                    client.sendImageWithURL(to, str(path))
                            except Exception as error:
                                 logError(error)
                                 var= traceback.print_tb(error.__traceback__)
                                 client.sendMessage(to,str(var))
                        elif cmd == "creepypasta" or cmd == " creepypasta":
                            r=requests.get("http://hipsterjesus.com/api")
                            data=r.text
                            data=json.loads(data)
                            hasil = "ã Creepypasta ã\n" 
                            hasil += str(data["text"])
                            client.sendMessage(msg.to, str(hasil))
                        elif cmd == "1cak" or cmd == " 1cak":
                            r=requests.get("http://api-1cak.herokuapp.com/random")
                            data=r.text
                            data=json.loads(data)
                            hasil = "ã 1CAK ã"                           
                            hasil += "\n\nId : " +str(data["id"])
                            hasil += "\nTitle : " + str(data["title"])                                                        
                            hasil += "\nLink : " + str(data["url"])
                            hasil += "\nVotes : " + str(data["votes"])
                            hasil += "\nNsfw : " + str(data["nsfw"])
                            image = str(data["img"])
                            client.sendImageWithURL(msg.to, str(image))
                            client.sendMessage(msg.to, str(hasil))                                 
                        elif cmd == "quote" or cmd == " quote":
                            r=requests.get("https://talaikis.com/api/quotes/random")
                            data=r.text
                            data=json.loads(data)
                            hasil = "ã Random Quote ã\n"
                            hasil += "Category : " +str(data["cat"])
                            hasil += "\n\n" +str(data["quote"])
                            hasil += "\n\n * * * " +str(data["author"])+ " * * *"
                            client.sendMessage(msg.to, str(hasil))
                        elif cmd.startswith("calc "):
                            query = cmd.replace("calc ","")
                            r=requests.get("https://www.calcatraz.com/calculator/api?c={}".format(urllib.parse.quote(query)))
                            data=r.text
                            data=json.loads(data)
                            client.sendMessage(msg.to, query + " = " + str(data))
#==============================================================================================================
                        elif cmd.startswith("meme "):
                            data = cmd.replace("meme ","")  
                            meme = data.split('|')
                            meme = meme[0].replace(' ','_')
                            atas = data.split('|')
                            atas = atas[1].replace(' ','_')
                            bawah = data.split('|')
                            bawah = bawah[2].replace(' ','_')
                            memes = 'https://memegen.link/'+meme+'/'+atas+'/'+bawah+'.jpg'
                            client.sendImageWithURL(msg.to, memes)
                        elif cmd == "rejectallz":
                            ginvited = client.ginvited
                            if ginvited != [] and ginvited != None:
                                for gid in ginvited:
                                    client.rejectGroupInvitation(gid)
                                client.sendMessage(to, "Berhasil tolak sebanyak {} undangan".format(str(len(ginvited))))
                            else:
                                client.sendMessage(to, "Tidak ada undangan yang tertunda")
#=========================================================================================
                        elif cmd.startswith("timezone "):
                            try:
                                search = cmd.replace("timezone ","")
                                r = requests.get("https://time.siswadi.com/geozone/{}".format(urllib.parse.quote(search)))
                                data=r.text
                                data=json.loads(data)
                                ret_ = "ã Timezone ã\n"
                                ret_ += "\nLatitude : " +str(data["data"]["latitude"])
                                ret_ += "\nLongitude : " +str(data["data"]["longitude"])
                                ret_ += "\nAddress : " +str(data["data"]["address"])
                                ret_ += "\nCountry : " +str(data["data"]["country"])
                                client.sendMessage(to, str(ret_))
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("à¸¢à¸¹à¸à¸¹à¸ "):
                            try:
                                search = cmd.replace("à¸¢à¸¹à¸à¸¹à¸ ","").strip()
                                query = urllib.parse.quote(search)
                                url = "https://youtube.com/results?search_query=" + query
                                response = urllib.request.urlopen(url)
                                html = response.read()
                                soup = BeautifulSoup(html, "html.parser")
                                results = soup.find(attrs={'class':'yt-uix-tile-link'})
                                dl = 'https://youtube.com/results?search_query=' + results['href']
                                vid = pafy.new(dl)
                                stream = vid.streams
                                for s in stream:
                                    vin = s.url
                                    hasil = "ã Youtube Video ã\n"
                                    hasil += "\nTitle : " + str(vid.title)
                                    hasil += "\nAuthor : " + str(vid.author)
                                    hasil += "\nDuration : " + str(vid.duration) + "ã " + s.quality + "ã"
                                    hasil += "\nRating : " + str(vid.rating)
                                    hasil += "\nView Count : " + str(vid.viewcount) + "x"
                                    hasil += "\nPublished : " + str(vid.published)
                                client.sendVideoWithURL(to, vin)
                                client.sendMessage(to, str(hasil))
                            except Exception as error:
                                client.sendMessage(to, "[ Error ]\n\n"+str(error))
                        elif cmd == "flipacoin" or cmd == " flipacoin":
                            sendMention(to, sender, "ã Flipacoin ã\nâ¢", "\nTossing coin, heads or tails?")
                            time.sleep(10)
                            sendMention(to, sender, "ã Flipacoin ã\nâ¢", "\n30 Seconds...")
                            time.sleep(10)
                            sendMention(to, sender, "ã Flipacoin ã\nâ¢", "\n20 Seconds...")
                            time.sleep(10)
                            sendMention(to, sender, "ã Flipacoin ã\nâ¢", "\n10 Seconds...")
                            message = ["\nHeads","\nTails"]
                            path = random.choice(message)
                            time.sleep(10)
                            sendMention(to, sender, "ã Flipacoin ã\nâ¢", "\nResult : " + str(path))
                        elif cmd == "guess" or cmd == " guess":
                            sendMention(to, sender, "ã Guess ã\nâ¢", "\nGetting random number 1-50")
                            time.sleep(10)
                            sendMention(to, sender, "ã Guess ã\nâ¢", "\n30 Seconds...")
                            time.sleep(10)
                            sendMention(to, sender, "ã Guess ã\nâ¢", "\n20 Seconds...")
                            time.sleep(10)
                            sendMention(to, sender, "ã Guess ã\nâ¢", "\n10 Seconds...")
                            path = random.randint(0,50)
                            time.sleep(10)
                            sendMention(to, sender, "ã Guess ã\nâ¢", "\nLucky number : " + str(path))
                        elif cmd == "à¸¥à¹à¸²à¸à¹à¸à¸·à¹à¸­à¸à¸à¸±à¹à¸à¸«à¸¡à¸" or cmd == " unfriendall":
                            try:
                                friend = client.getContacts(client.getAllContactIds())
                                client.sendMessage(to,"à¸à¸¸à¸à¹à¸à¹à¸¥à¹à¸²à¸à¹à¸à¸·à¹à¸­à¸à¸à¸±à¹à¸à¸«à¸¡à¸ {} à¸à¸".format(len(friend)))
                                for unfriend in friend:
                                    client.deleteContact(unfriend.mid)
                                client.sendMessage(to,"à¸à¸¸à¸à¹à¸à¹à¸¥à¹à¸²à¸à¹à¸à¸·à¹à¸­à¸à¸à¸±à¹à¸à¸«à¸¡à¸ {} à¸à¸".format(len(friend)))
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd == "clearallinvites" or cmd == "rejectall":
                            group = client.getGroupIdsInvited()
                            for reject in group:
                                client.rejectGroupInvitation(reject)
                            client.sendMessage(to, "success")
                        elif cmd == "makers" or cmd == "creator":
                            sendMention(to, sender, "ã Auto Mentions ã\nâ¢", "\nThis is my Creator..")
                            client.sendContact(to, "uaca55463c423c3632012598148691da7")
                        elif cmd == " name" or cmd == "name":
                            h = client.getContact(clientMID)
                            sendMention(to, sender, "ã Auto Mention ã\nâ¢", "\nDisplay Name : \n" + str(h.displayName))
                        elif cmd == " status" or cmd == "stats":
                            h = client.getContact(clientMID)
                            sendMention(to, sender, "ã Auto Mention ã\nâ¢", "\nStatus Message : \n" + str(h.statusMessage))
                        elif cmd == " picture" or cmd == "picture":
                            h = client.getContact(clientMID)
                            sendMention(to, sender, "ã Auto Mention ã\nâ¢", "\nThis is my picture...")
                            client.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + h.pictureStatus)
                        elif cmd == " cover" or cmd == "cover":
                            cu = client.getProfileCoverURL(clientMID)          
                            path = str(cu)
                            sendMention(to, sender, "ã Auto Mention ã\nâ¢", "\nThis is my cover...")
                            client.sendImageWithURL(msg.to, path)
                        elif cmd == " video" or cmd == "video":
                            h = client.getContact(clientMID)
                            sendMention(to, sender, "ã Auto Mention ã\nâ¢", "\nThis is my video...")
                            client.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/{}/vp".format(str(h.pictureStatus)))
                        elif cmd == "raffle" or cmd == " raffle":
                            group = client.getGroup(to)
                            try:
                                members = [mem.mid for mem in group.members]
                            except:
                                members = [mem.mid for mem in group.members]
                            message = random.choice(members)
                            sendMention(to, sender, "ã Raffle ã\nâ¢", "\nWinner is...")
                            client.sendContact(to, message)
                        elif cmd == "raffle2" or cmd == " raffle2":
                            group = client.getGroup(to)
                            try:
                                members = [mem.mid for mem in group.members]
                            except:
                                members = [mem.mid for mem in group.members]
                            message = random.choice(members)
                            sendMention(to, sender, "ã Raffle2 ã\nâ¢", "\nLoser is...")
                            client.sendContact(to, message)
                        elif cmd == "tespeed" or cmd == "sp":
                            try:
                                start = time.time()
                                client.sendMessage(to, "à¸à¸³à¸¥à¸±à¸à¸à¸à¸ªà¸­à¸...")
                                elapsed_time = time.time() - start
                                client.sendMessage(to,"Time:\n%s"%str(round(elapsed_time,3)))
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd.startswith("$ "):
                            query = cmd.replace("$ ","")
                            s = os.popen(query)
                            p = s.read()
                            client.sendMessage(to,p)
                        elif cmd.startswith("biography "):
                            query = cmd.replace("biography ","")
                            cond = query.split("|")
                            search = str(cond[0])
                            result = requests.get("https://farzain.xyz/api/biografi.php?apikey=YcUTTUvO2xe75rxWhsqSkWkZsIeTn9&id={}".format(str(search)))
                            data = result.text
                            data = json.loads(data)
                            if len(cond) == 1:
                                num = 0
                                ret_ = " ã Biography ã\nType: Search Biography"
                                for bio in data:
                                    num += 1
                                    ret_ += "\n{}. {}".format(str(num), str(bio["title"]))                                        
                                ret_ += "\n\nExample: Biography {}|1".format(settings["keyCommand"],search)
                                client.sendMessage(to, str(ret_))
                            elif len(cond) == 2:
                                num = int(cond[1])
                                if num <= len(data):
                                    bio = data[num - 1]
                                    result = requests.get("https://farzain.xyz/api/biografi.php?apikey=YcUTTUvO2xe75rxWhsqSkWkZsIeTn9&id={}".format(str(search)))
                                    data = result.text
                                    data = json.loads(data)
                                    ret_ = " ã Biography ã\nType: Detail Biography"                                        
                                    ret_ += "\n    {}".format(str(bio["link"]))
                                    client.sendImageWithURL(to, str(bio["img"]))
                                    client.sendMessage(to, str(ret_))
                        elif cmd.startswith("sendfile"):
                               if sender in admin:
                                   sep = text.split(" ")
                                   file = text.replace(sep[0] + " ","")
             #                     sendMention(to,"[ Send File ]\nType: Send Files\nI Am Send Your Files @!Please Wait",[sender])
                                   time.sleep(1)
                                   client.sendFile(to,file)
                        elif cmd.startswith("ginfo# "):
                            number = cmd.replace("ginfo# ","")
                            groups = client.getGroupIdsJoined()
                            ret_ = ""
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                path = "http://dl.profile.line-cdn.net/" + G.pictureStatus
                                try:
                                    gCreator = G.creator.displayName
                                except:
                                    gCreator = "Tidak ditemukan"
                                if G.invitee is None:
                                    gPending = "0"
                                else:
                                    gPending = str(len(G.invitee))
                                if G.preventedJoinByTicket == True:
                                    gQr = "Tertutup"
                                    gTicket = "Tidak ada"
                                else:
                                    gQr = "Terbuka"
                                    gTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(G.id)))
                                timeCreated = []
                                timeCreated.append(time.strftime("%d-%m-%Y [ %H:%M:%S ]", time.localtime(int(G.createdTime) / 1000)))
                                ret_ += "ã Group Info ã\n"
                                ret_ += "\nNama Group : {}".format(G.name)
                                ret_ += "\nID Group : {}".format(G.id)
                                ret_ += "\nPembuat : {}".format(gCreator)
                                ret_ += "\nWaktu Dibuat : {}".format(str(timeCreated))
                                ret_ += "\nJumlah Member : {}".format(str(len(G.members)))
                                ret_ += "\nJumlah Pending : {}".format(gPending)
                                ret_ += "\nGroup Qr : {}".format(gQr)
                                ret_ += "\nGroup Ticket : {}".format(gTicket)
                                client.sendImageWithURL(to, path)
                                client.sendMessage(to, str(ret_))
                                client.sendContact(to, G.creator.mid)
                            except:
                                pass
                        elif cmd.startswith("closeqr#"):
                            number = cmd.replace("closeqr#","")
                            groups = client.getGroupIdsJoined()
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    G.preventedJoinByTicket = True
                                    client.updateGroup(G)
                                except:
                                    G.preventedJoinByTicket = True
                                    client.updateGroup(G)
                                client.sendMessage(to, "ã Close Qr ã\n\nGroup : " + G.name)
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("openqr#"):
                            number = cmd.replace("openqr#","")
                            groups = client.getGroupIdsJoined()
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    G.preventedJoinByTicket = False
                                    client.updateGroup(G)
                                    gurl = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(G.id)))
                                except:
                                    G.preventedJoinByTicket = False
                                    client.updateGroup(G)
                                    gurl = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(G.id)))
                                client.sendMessage(to, "ã Open Qr ã\n\nGroup : " + G.name + "\nLink: " + gurl)
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("leave#"):
                            number = cmd.replace("leave#","")
                            groups = client.getGroupIdsJoined()
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    client.leaveGroup(G.id)
                                except:
                                    client.leaveGroup(G.id)
                                client.sendMessage(to, "ã Leave ã\n\nGroup : " + G.name)
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("member# "):
                            number = cmd.replace("member# ","")
                            groups = client.getGroupIdsJoined()
                            ret_ = ""
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                no = 0
                                ret_ = "ã Member List ã\n"
                                for mem in G.members:
                                    no += 1
                                    ret_ += "\n " + str(no) + ". " + mem.displayName
                                client.sendMessage(to,"Member in Group : \n"+ str(G.name) + "\n\n" + ret_ + "\n\nTotal : %i Members" % len(G.members))
                            except: 
                                pass
                        elif cmd == "à¸à¹à¸­à¸¡à¸¹à¸¥à¸à¸¥à¸¸à¹à¸¡" or cmd == "à¸à¹à¸­à¸¡à¸¹à¸¥à¸à¸¥à¸¸à¹à¸¡":
                            group = client.getGroup(to)
                            path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                            try:
                                gCreator = group.creator.displayName
                            except:
                                gCreator = "Tidak ditemukan"
                            if group.invitee is None:
                                gPending = "0"
                            else:
                                gPending = str(len(group.invitee))
                            if group.preventedJoinByTicket == True:
                                gQr = "Tertutup"
                                gTicket = "Tidak ada"
                            else:
                                gQr = "Terbuka"
                                gTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
                            timeCreated = []
                            timeCreated.append(time.strftime("%d-%m-%Y [ %H:%M:%S ]", time.localtime(int(group.createdTime) / 1000)))
                            ret_ = "ã à¸à¹à¸­à¸¡à¸¹à¸¥à¸à¸¥à¸¸à¹à¸¡ ã\n"
                            ret_ += "\nà¸à¸´à¹à¸­à¸à¸¥à¸¸à¹à¸¡ : {}".format(group.name)
                            ret_ += "\nà¹à¸­à¸à¸µà¸à¸¥à¸¸à¹à¸¡ : {}".format(group.id)
                            ret_ += "\nà¸à¸·à¹à¸´à¸­à¸à¸à¸ªà¸£à¹à¸²à¸ : {}".format(gCreator)
                            ret_ += "\nà¸ªà¸£à¹à¸²à¸à¹à¸¡à¸·à¹à¸­ : {}".format(str(timeCreated))
                            ret_ += "\nà¸ªà¸¡à¸²à¸à¸´à¸à¹à¸à¸à¸¥à¸¸à¹à¸¡ : {}".format(str(len(group.members)))
                            ret_ += "\nà¸à¹à¸²à¸à¹à¸à¸´à¸ : {}".format(gPending)
                            ret_ += "\nà¸à¸¥à¸¸à¹à¸¡  : {}".format(gQr)
                            ret_ += "\nà¸¥à¸´à¹à¸à¸à¸¥à¸¸à¹à¸¡ : {}".format(gTicket)
                            client.sendImageWithURL(to, path)
                            client.sendMessage(to, str(ret_))
                            client.sendContact(to, group.creator.mid)
                        elif cmd.startswith("friendinfo# "):
                            separate = msg.text.split(" ")
                            number = msg.text.replace(separate[0] + " ","")
                            contactlist = client.getAllContactIds()
                            try:
                                contact = contactlist[int(number)-1]
                                friend = client.getContact(contact)
                                cu = client.getProfileCoverURL(contact)
                                path = str(cu)
                                image = "http://dl.profile.line-cdn.net/" + friend.pictureStatus
                                try:
                                    client.sendMessage(to,"ã Friend Info ã\n\n" + "Name : " + friend.displayName + "\nStatus : " + friend.statusMessage + "\nMid : " + friend.mid)
                                    client.sendImageWithURL(to,image)
                                    client.sendImageWithURL(to,path)
                                    client.sendContact(to, friend.mid)
                                except:
                                    pass
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd == "à¸à¹à¸²à¸" or cmd == "à¸à¹à¸²à¸":
                            groups = client.getGroupIdsJoined()
                            ret_ = "ã à¸à¸¥à¸¸à¹à¸¡à¸à¸±à¹à¸à¸«à¸¡à¸ ã"
                            no = 1
                            for gid in groups:
                                group = client.getGroup(gid)
                                ret_ += "\n{}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                                no = (no+1)
                            ret_ += "\nã à¸à¸±à¹à¸à¸«à¸¡à¸ : {} à¸à¸¥à¸¸à¹à¸¡ ã".format(str(len(groups)))
                            ret_ += "\nUsage : Ginfo# number"
                            client.sendMessage(to, str(ret_))
                        elif cmd.startswith("à¸ªà¸§à¸±à¸ªà¸à¸µ "):
                            try:
                                if msg.toType == 2:
                                    name = cmd.replace("à¸ªà¸§à¸±à¸ªà¸à¸µ ","")
                                    groups = client.getGroup(msg.to)
                                    targets = []
                                    for group in groups.members:
                                        if name in group.displayName.lower():
                                            targets.append(group.mid)
                                    if targets == []:
                                        client.sendMessage(to, "User Not found.")
                                    else:
                                        for target in targets:
                                            try:
                                                a = "ã Whois ã\n"
                                                a += "\nà¸à¸·à¹à¸­ : " + client.getContact(target).displayName
                                                a += "\nMention : @!    "
                                                a += "\nà¸à¸±à¸ª : " + client.getContact(target).statusMessage
                                                a += "\nà¹à¸­à¸à¸µ : " + target
                                                khieMention(to, str(a),[target])
                                                client.sendContact(to, target)
                                            except:
                                                pass
                            except Exception as error:
                                client.sendMessage(to, str(error))
                            
                        elif cmd == "à¸à¹à¸­à¸¡à¸¹à¸¥" or cmd == "about":
                            try:
                                arr = []
                                owner = "u4862fe4b182b2fd194a3108e2f3662e8"
                                khietag = "u4862fe4b182b2fd194a3108e2f3662e8"                        
             #                   creator = client.getContact(owner)
                                contact = client.getContact(clientMID)
                                grouplist = client.getGroupIdsJoined()
                                contactlist = client.getAllContactIds()
                                favoritelist = client.getFavoriteMids()
                                blockedlist = client.getBlockedContactIds()
                                ret_ = "ãà¸à¹à¸­à¸¡à¸¹à¸¥ã\n"
                                ret_ += "\nð à¸à¸·à¹à¸­à¹à¸£à¸² â£ {}".format(contact.displayName)
                                ret_ += "\nð à¸à¸¥à¸¸à¹à¸¡à¸à¸µà¹à¸­à¸¢à¸¹à¹ â£ {}".format(str(len(grouplist)))
                                ret_ += "\nð à¹à¸à¸·à¹à¸­à¸ â£ {}".format(str(len(contactlist)))
                                ret_ += "\nð Favorites â£ {}".format(str(len(favoritelist)))
                                ret_ += "\nð à¸à¸¥à¹à¸­à¸ â£ {}".format(str(len(blockedlist)))
                                ret_ += "\nð Bot Version â£ V.03"
                                ret_ += "\nð à¸à¸à¸ªà¸£à¹à¸²à¸ â£ @!              " #.format(creator.displayName)
   #                             client.sendMessage(to, str(ret_))
                                khieMention(to, str(ret_),[khietag])
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd == 'square' or cmd == ' squares':
                            a = client.getJoinedSquares()
                            squares = a.squares
                            txt2 = 'ã Squares ã\n'
                            for s in range(len(squares)):
                                txt2 += "\n"+str(s+1)+". "+str(squares[s].name)
                            txt2 += "\n\nTotal {} Squares.".format(str(len(squares)))
                            txt2 += "\n\nUsage : Square#num"
                            client.sendMessage(to,str(txt2))
                        elif cmd.startswith("crash#"):
                            number = cmd.replace("crash#","")
                            groups = client.getGroupIdsJoined()
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    client.sendContact(group, "uc7d319b7d2d38c35ef2b808e3a2aeed9',")
                                except:
                                    client.sendContact(group, "uc7d319b7d2d38c35ef2b808e3a2aeed9',")
                                client.sendMessage(to, "ã Remote Crash ã\n\nGroup : " + G.name)
                            except Exception as error:
                                client.sendMessage(to, str(error))
                                        
                        elif cmd.startswith("square#"):
                            number = cmd.replace("square#","")
                            squares = client.getJoinedSquares().squares
                            ret_ = "ã Square ã\n"
                            try:
                                square = squares[int(number)-1]
                                path = "http://dl.profile.line-cdn.net/" + square.profileImageObsHash
                                ret_ += "\n1. Name : {}".format(str(square.name))
                                ret_ += "\n2. Description: {}".format(str(square.desc))
                                ret_ += "\n3. ID Square : {}".format(str(square.mid))
                                ret_ += "\n4. Link : {}".format(str(square.invitationURL))
                                client.sendImageWithURL(to, path)
                                client.sendMessage(to, str(ret_))
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("ats#"):
                            number = cmd.replace("ats#","")
                            groups = client.getGroupIdsJoined()
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    contact = [mem.mid for mem in G.members]
                                    text = "Mention %i User\n" %len(contact)
                                    no = 1
                                    for mid in contact:
                                        text += "\n{}. @!           ".format(str(no))
                                        no = (no+1)
                                    text += "\n\n {} ".format(str(G.name))
                                    khieMention(group, text, contact)
                                except:
                                    contact = [mem.mid for mem in G.members]
                                    text = "Mention %i User \n" %len(contact)
                                    no = 1
                                    for mid in contact:
                                        text += "\n{}. @!           ".format(str(no))
                                        no = (no+1)
                                    text += "\n\n{} ".format(str(G.name))
                                    khieMention(group, text, contact)
                                client.sendMessage(to, "Remote Ats Succes\n\nIn Group : " + G.name)
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("à¹à¸à¸·à¹à¸­à¸"):
                            contactlist = client.getAllContactIds()
                            kontak = client.getContacts(contactlist)
                            num=1
                            msgs="ã à¸£à¸²à¸¢à¸à¸·à¹à¸­à¹à¸à¸·à¹à¸­à¸ ã\n"
                            for ids in kontak:
                                msgs+="\n%i. %s" % (num, ids.displayName)
                                num=(num+1)
                            msgs+="\n\nTotal : %i Friends" % len(kontak)
                            msgs+= "\n\nUsage : Friendinfo# number"
                            client.sendMessage(to, msgs)
                        elif cmd.startswith("favoritelist"):
                            contactlist = client.getFavoriteMids()
                            kontak = client.getContacts(contactlist)
                            num=1
                            msgs="ã Favorite List ã\n"
                            for ids in kontak:
                                msgs+="\n%i. %s" % (num, ids.displayName)
                                num=(num+1)
                            msgs+="\n\nTotal : %i Favorites" % len(kontak)
                            msgs+= "\n\nUsage : {}Favoriteinfo# number".format(settings["keyCommand"])
                            client.sendMessage(to, msgs)
                        elif cmd.startswith("favoriteinfo# "):
                            separate = msg.text.split(" ")
                            number = msg.text.replace(separate[0] + " ","")
                            contactlist = client.getFavoriteMids()
                            try:
                                contact = contactlist[int(number)-1]
                                friend = client.getContact(contact)
                                cu = client.getProfileCoverURL(contact)
                                path = str(cu)
                                image = "http://dl.profile.line-cdn.net/" + friend.pictureStatus
                                try:
                                    client.sendMessage(to,"ã Favorite Info ã\n\n" + "Name : " + friend.displayName + "\nStatus : " + friend.statusMessage + "\nMid : " + friend.mid)
                                    client.sendImageWithURL(to,image)
                                    client.sendImageWithURL(to,path)
                                    client.sendContact(to, friend.mid)
                                except:
                                    pass
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd == "motivate" or cmd == " ":
                            r = requests.get("https://talaikis.com/api/quotes/random")
                            data=r.text
                            data=json.loads(data)                                                                   
                            client.sendMessage(to,str(data["quote"]))
                        elif cmd == "bitcoin" or cmd == " bitcoin":
                            r=requests.get("https://xeonwz.herokuapp.com/bitcoin.api")
                            data=r.text
                            data=json.loads(data)
                            hasil = "ã Bitcoin ã\n" 
                            hasil += "\nPrice : " +str(data["btc"])
                            hasil += "\nExpensive : " +str(data["high"])
                            hasil += "\nCheap : " +str(data["low"])
                            client.sendMessage(msg.to, str(hasil))
                        elif cmd.startswith("suggestion "):
                            query = cmd.replace("suggestion ","")
                            r=requests.get("http://api.ntcorp.us/se/v1/?q={}".format(urllib.parse.quote(query)))
                            data=r.text
                            data=json.loads(data)
                            no = 0
                            ret_ = "ãSuggestionã\n"                                                                                                                       
                            anu = data["result"]["suggestions"]
                            for s in anu:
                                hmm = s
                                no += 1
                                ret_ += "\n" + str(no) + ". " + "{}".format(str(hmm))
                            client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("à¸à¸¥à¹à¸­à¸à¹à¸­à¸à¸µ "):
                            user = cmd.replace("à¸à¸¥à¹à¸­à¸à¹à¸­à¸à¸µ ","")
                            client.blockContact(user)
                            client.sendMessage(to, "à¸à¸³à¸à¸²à¸£à¸à¸¥à¹à¸­à¸à¹à¸­à¸à¸µà¸à¸±à¹à¸à¹à¸¥à¹à¸§")
                                
                        elif cmd.startswith("prankcall "):
                            sep = msg.text.split(" ")
                            nomor = text.replace(sep[0] + " ","")
                            r = requests.get("http://apisora2.herokuapp.com/prank/call/?no={}".format(urllib.parse.quote(nomor)))
                            data = r.text
                            data = json.loads(data)
                            ret_ = "Prangked Call :"
                            ret_ += "\nStatus : {}".format(str(data["status"]))
                            ret_ += "\nTarget "+str(data["result"])
                            client.sendMessage(msg.to, str(ret_))

                        elif cmd.startswith("à¹à¸­à¸à¸µà¹à¸¥à¸à¹ "):
                            id = cmd.replace("à¹à¸­à¸à¸µà¹à¸¥à¸à¹ ","")
                            conn = client.findContactsByUserid(id)
                            if True:                                      
                                client.sendMessage(to,"http://line.me/ti/p/~" + id)
                                client.sendContact(to,conn.mid)
                        elif cmd.startswith("à¸à¸¹à¸à¸à¸¸à¸à¸«à¹à¸­à¸ "):
                                bctxt = cmd.replace("gcastvoice ", "")
                                bc = ("Broadcast voice by khie")
                                cb = (bctxt + bc)
                                tts = gTTS(cb, lang='th', slow=False)
                                tts.save('tts.mp3')
                                n = client.getGroupIdsJoined()
                                for manusia in n:
                                    client.sendAudio(manusia, 'tts.mp3')
                        elif cmd.startswith("fdcastvoice "):
                                bctxt = cmd.replace("fdcastvoice ", "")
                                bc = ("Broadcast voice by khie")
                                cb = (bctxt + bc)
                                tts = gTTS(cb, lang='id', slow=False)
                                tts.save('tts.mp3')
                                n = client.getAllContactIdsJoined()
                                for manusia in n:
                                    client.sendAudio(manusia, 'tts.mp3')
                        elif cmd.startswith("infomovie "):
                            query = cmd.replace("infomovie ","")   
                            r = requests.get("https://farzain.xyz/api/film.php?id={}".format(str(query)))
                            data1 = r.text
                            data1 = json.loads(data1)
                            hasil="Imdb Result:\n"
                            hasil += "\nTitle: {}".format(str(data1["Title"]))
                            hasil += "\nYear: {}".format(str(data1["Year"]))
                            hasil += "\n Rating: {}".format(str(data1["Rated"]))
                            hasil += "\nRelease: {}".format(str(data1["Released"]))
                            hasil += "\nDuration: {}".format(str(data1["Runtime"]))
                            hasil += "\nDirector: {}".format(str(data1["Director"]))
                            hasil += "\nWritter: {}".format(str(data1["Writer"]))
                            hasil += "\nActor: {}".format(str(data1["Actors"]))
                            hasil += "\n\n{}".format(str(data1["Plot"]))
                            hasil += "\n\nAwards: {}".format(str(data1["Awards"]))
                            client.sendImageWithURL(to,str(data1["Poster"]))
                            client.sendMessage(to, str(hasil))
                        elif cmd.startswith("status "):
                            if msg.toType == 2:                   
                                _name = cmd.replace("status ","")
                                gs = client.getGroup(to)
                                targets = []
                                for g in gs.members:
                                    if _name in g.displayName.lower():
                                        targets.append(g.mid)
                                        if targets == []:
                                            client.sendMessage(to,"Not found.")
                                        else:
                                            for target in targets:
                                                try:
                                                    M = Message()
                                                    M.to = to
                                                    M.contentType = 13
                                                    M.contentMetadata = {'mid': target}
                                                    client.sendMessage(to, client.getContact(target).displayName+":\n" + client.getContact(target).statusMessage)                                                            
                                                except:
                                                    pass
                        elif cmd.startswith("prankmsg "):
                            sep = msg.text.split(" ")
                            nomor = text.replace(sep[0] + " ","")
                            r = requests.get("http://apisora2.herokuapp.com/prank/sms/?no={}".format(urllib.parse.quote(nomor)))
                            data = r.text
                            data = json.loads(data)
                            ret_ = "Prangked Message :"
                            ret_ += "\nStatus : {}".format(str(data["status"]))
                            ret_ += "\nTarget "+str(data["result"])
                            client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("unblockmid "):
                            user = cmd.replace("unblockmid ","")
                            client.unblockContact(user)
                            client.sendMessage(to, "Success Unblock Contact.")    
                        elif cmd == "à¸à¸¥à¹à¸­à¸" or cmd == " blocklist":
                            blockedlist = client.getBlockedContactIds()
                            kontak = client.getContacts(blockedlist)
                            num=1
                            msgs="ã à¸£à¸²à¸¢à¸à¸·à¹à¸­à¸à¸à¸à¸µà¹à¹à¸£à¸²à¸à¸¥à¹à¸­à¸ ã\n"
                            for ids in kontak:
                               msgs+="\n%i. %s" % (num, ids.displayName)
                               num=(num+1)
                            msgs+="\n\nTotal : %i Blocks" % len(kontak)
                            msgs+= "\n\nUsage : Blockinfo <num>"
                            client.sendMessage(to, msgs)
                        elif cmd == "group pending" or cmd == " groups pending":
                            groups = client.getGroupIdsInvited()
                            ret_ = "ã Group Pending List ã\n"
                            no = 1
                            for gid in groups:
                                group = client.getGroup(gid)
                                ret_ += "\n{}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                                no = (no+1)
                            ret_ += "\n\nTotal {} Pending".format(str(len(groups)))
                            ret_ += "\n\nUsage : Reject #number"
                            client.sendMessage(to, str(ret_))
                            
                        elif cmd.startswith("à¸¥à¸à¸£à¸±à¸"):
                            number = cmd.replace("à¸¥à¸à¸£à¸±à¸","")
                            groups = client.getGroupIdsInvited()
                            try:
                                group = groups[int(number)-1]
                                G = client.getGroup(group)
                                try:
                                    client.rejectGroupInvitation(G.id)
                                except:
                                    client.rejectGroupInvitation(G.id)
                                client.sendMessage(to, "ã Reject ã\n\nGroup : " + G.name)
                            except Exception as error:
                                client.sendMessage(to, str(error))
                        elif cmd.startswith("announcetext "):
                           Text = cmd.replace("announcetext ","")
                           Link = "http://line.me/ti/p/uv8Cqx77tB"
                           Logo = "http://dl.profile.line-cdn.net/" + client.getGroup(to).pictureStatus
                           stype = 1
                           announce = ChatRoomAnnouncementContents(displayFields=5,text=Text,link=Link,thumbnail=Logo)
                           client.createChatRoomAnnouncement(to,stype,announce)
                           sendMention(receiver, sender, "ã Create Announce ã\nType : Lock\nâ¢", "\nSuccess Create Announce Lock "+str(Text)+" in Group : "+str(client.getGroup(to).name))
                        elif cmd.startswith("blockinfo "):
                            number = cmd.replace("blockinfo ","")
                            contactlist = client.getBlockedContactIds()
                            try:
                                contact = contactlist[int(number)-1]
                                friend = client.getContact(contact)
                                cu = client.getProfileCoverURL(contact)
                                path = str(cu)
                                image = "http://dl.profile.line-cdn.net/" + friend.pictureStatus
                                try:
                                    client.sendMessage(to,"ã Block Info ã\n\n" + "Name : " + friend.displayName + "\nStatus : " + friend.statusMessage + "\nMid : " + friend.mid)
                                    client.sendImageWithURL(to,image)
                                    client.sendImageWithURL(to,path)
                                    client.sendContact(to, friend.mid)
                                except:
                                    pass
                            except Exception as error:
                                client.sendMessage(to, "ã Result Error ã\n" + str(error))
                        elif cmd.startswith("Instagram "):
                            try:
                                search = cmd.replace("instagram ","")
                                r=requests.get("http://rahandiapi.herokuapp.com/instainfo/"+search+"?key=betakey")
                                data = r.text
                                data = json.loads(data)
                                if data != []:
                                    ret_ = " \nInstagram"
                                    ret_ += "\nName: {}".format(str(data["result"]["name"]))
                                    ret_ += "\nUsername: {}".format(str(data["result"]["username"]))                 
                                    ret_ += "\n\n{}".format(str(data["result"]["bio"]))            
                                    ret_ += "\n\nFollowers: {}".format(str(data["result"]["follower"]))
                                    ret_ += "\nFollowing: {}".format(str(data["result"]["following"]))                                 
                                    ret_ += "\nTotal Post: {}".format(str(data["result"]["mediacount"]))
                                    ret_ += "\nhttps://www.instagram.com/{}".format(search)
                                    path = data["result"]["url"]
                                    client.sendImageWithURL(to, str(path))
                                    client.sendMessage(to, str(ret_))
                            except Exception as error:
                                logError(error)
                                var= traceback.print_tb(error.__traceback__)
                                client.sendMessage(to,str(var))
                        elif cmd.startswith("à¸¢à¸à¹à¸¥à¸´à¸ "):
                            args = cmd.replace("à¸¢à¸à¹à¸¥à¸´à¸ ","")
                            mes = 0
                            try:
                                mes = int(args[1])
                            except:
                                mes = 1
                            M = client.getRecentMessagesV2(to, 101)
                            MId = []
                            for ind,i in enumerate(M):
                                if ind == 0:
                                    pass
                                else:
                                    if i._from == client.profile.mid:
                                        MId.append(i.id)
                                        if len(MId) == mes:
                                            break
                            def unsMes(id):
                                client.unsendMessage(id)
                            for i in MId:
                                thread1 = threading.Thread(target=unsMes, args=(i,))
                                thread1.start()
                                thread1.join()
                            client.sendMessage(to, ' ã à¸à¸³à¸¥à¸±à¸à¸¢à¸à¹à¸¥à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡ ã\nà¸¢à¸à¹à¸¥à¸´à¸à¸à¹à¸­à¸à¸§à¸²à¸¡à¸à¸±à¹à¸à¸«à¸¡à¸ {} à¸à¹à¸­à¸à¸§à¸²à¸¡'.format(len(MId)))
                        elif cmd.startswith("fc "):
                            sep = msg.text.split(" ")
                            anu = msg.text.replace(sep[0] + " "," ")                
                            with requests.session() as web:
                                web.headers["user-agent"] = random.choice(settings["userAgent"])
                                r = web.get("https://farzain.xyz/api/premium/fs.php?apikey=apikey_saintsbot&id={}".format(urllib.parse.quote(anu)))
                                data = r.text
                                data = json.loads(data)
                                if data["status"] == "success":
                                    ret_ = data["url"]
                                    client.sendImageWithURL(msg.to,ret_)
                                else:
                                    client.sendMessage(msg.to, "Error")
                        elif cmd.startswith(".speed"):
                                get_profile_time_start = time.time()
                                get_profile = client.getProfile()
                                get_profile_time = time.time() - get_profile_time_start
                                get_group_time_start = time.time()
                                get_group = client.getGroupIdsJoined()
                                get_group_time = time.time() - get_group_time_start
                                get_contact_time_start = time.time()
   #                              get_contact = client.getContact(clientMid)
                                get_contact_time = time.time() - get_contact_time_start
                   #              client.sendMessage("u4862fe4b182b2fd194a3108e2f3662e8", '.')
                                client.sendMessage(to, "Time:\n%.6f" % (get_group_time/3))

                        elif cmd.startswith("zodiaceng "):
                            string = cmd.replace("zodiaceng ","")   
                            r=requests.get("http://horoscope-api.herokuapp.com/horoscope/week/{}".format(str(string)))
                            data=r.text
                            data=json.loads(data)
                            hasil="Zodiac Result:\n"
                            hasil += "\nZodiac: " +str(data["sunsign"])
                            hasil += "\n\n"+str(data["horoscope"])
                            hasil += "\n\nDate: " +str(data["week"])                                                                                                                                                          
                            client.sendMessage(to,str(hasil))
                        elif cmd.startswith("zodiac "):
                            sep = msg.text.split(" ")
                            query = text.replace(sep[0] + " ","")
                            r = requests.post("https://aztro.herokuapp.com/?sign={}&day=today".format(urllib.parse.quote(query)))
                            data = r.text
                            data = json.loads(data)
                            data1 = data["description"]
                            data2 = data["color"]
                            translator = Translator()
                            hasil = translator.translate(data1, dest='id')
                            hasil1 = translator.translate(data2, dest='id')
                            A = hasil.text
                            B = hasil1.text
                            ret_ = "Ramalan zodiak {} hari ini \n".format(str(query))
                            ret_ += str(A)
                            ret_ += "\n\nTanggal : " +str(data["current_date"])
                            ret_ += "\nRasi bintang : "+query
                            ret_ += " ("+str(data["date_range"]+")")
                            ret_ += "\nPasangan Zodiak : " +str(data["compatibility"])
                            ret_ += "\nAngka keberuntungan : " +str(data["lucky_number"])
                            ret_ += "\nWaktu keberuntungan : " +str(data["lucky_time"])
                            ret_ += "\nWarna kesukaan : " +str(B)
                            client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("urban "):
                            sep = cmd.split(" ")
                            judul = cmd.replace(sep[0] + " ","")
                            url = "http://api.urbandictionary.com/v0/define?term="+str(judul)
                            with requests.session() as s:
                                s.headers["User-Agent"] = random.choice(settings["userAgent"])
                                r = s.get(url)
                                data = r.text
                                data = json.loads(data)
                                y = "Result Urban :"
                                y += "\nTags: "+ data["tags"][0]
                                y += ","+ data["tags"][1]
                                y += ","+ data["tags"][2]
                                y += ","+ data["tags"][3]
                                y += ","+ data["tags"][4]
                                y += ","+ data["tags"][5]
                                y += ","+ data["tags"][6]
                                y += ","+ data["tags"][7]
                                y += "\n\nAuthor: "+str(data["list"][0]["author"])
                                y += "\nWord: "+str(data["list"][0]["word"])
                                y += "\nLink: "+str(data["list"][0]["permalink"])
                                y += "\nDefinition: "+str(data["list"][0]["definition"])
                                y += "\nExample: "+str(data["list"][0]["example"])
                                client.sendMessage(to, str(y))
                        elif cmd.startswith("zodiacind "):
                            sep = msg.text.split(" ")
                            url = msg.text.replace(sep[0] + " ","")    
                            with requests.session() as s:
                                s.headers['user-agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                                r = s.get("https://www.vemale.com/zodiak/{}".format(urllib.parse.quote(url)))
                                soup = BeautifulSoup(r.content, 'html5lib')
                                ret_ = ""
                                for a in soup.select('div.vml-zodiak-detail'):
                                    ret_ += a.h1.string
                                    ret_ += "\n"+ a.h4.string
                                    ret_ += " : "+ a.span.string +""
                                for b in soup.select('div.col-center'):
                                    ret_ += "\nTanggal : "+ b.string
                                for d in soup.select('div.number-zodiak'):
                                    ret_ += "\nAngka keberuntungan : "+ d.string
                                for c in soup.select('div.paragraph-left'):
                                    ta = c.text
                                    tab = ta.replace("    ", "")
                                    tabs = tab.replace(".", ".\n")
                                    ret_ += "\n"+ tabs
                                    #print (ret_)
                                client.sendMessage(msg.to, str(ret_))
                        elif cmd.startswith("searchporn "):
                            kata = cmd.replace("searchporn", "")
                            with _session as web:
                                try:
                                    r = web.get("https://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&search={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    ret_ = "Porns Link\n"
                                    no = 1
                                    anu = data["videos"]
                                    if len(anu) >= 5:
                                        for s in range(5):
                                            hmm = anu[s]
                                            title = hmm['video']['title']
                                            duration = hmm['video']['duration']
                                            views = hmm['video']['views']
                                            link = hmm['video']['embed_url']
                                            ret_ += "\n\n{}. Title : {}\n    Duration : {}\n    Views : {}\n    Link : {}".format(str(no), str(title), str(duration), str(views), str(link))
                                            no += 1
                                    else:
                                        for s in anu:
                                            hmm = s
                                            title = hmm['video']['title']
                                            duration = hmm['video']['duration']
                                            views = hmm['video']['views']
                                            link = hmm['video']['embed_url']
                                            ret_ += "\n\n{}. Title : {}\n    Duration : {}\n    Views : {}\n    Link : {}".format(str(no), str(title), str(duration), str(views), str(link))
                                            no += 1
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "Porn Not Found !")
                        elif cmd == "à¸à¹à¸²à¸§":
                             try:
                                 api_key = "ue4117356009586eb55366d1199e56589"
                                 r = _session.get("https://newsapi.org/v2/top-headlines?country=id&apiKey={}".format(str(api_key)))
                                 data = r.text
                                 data = json.loads(data)
                                 ret_ = "Top News\n"
                                 no = 1
                                 anu = data["articles"]
                                 if len(anu) >= 5:
                                     for s in range(5):
                                         syit = anu[s]
                                         sumber = syit['source']['name']
                                         author = syit['author']
                                         judul = syit['title']
                                         url = syit['url']
                                         ret_ += "\n\n{}. Title : {}\n    Sumber : {}\n    Penulis : {}\n    Link : {}".format(str(no), str(judul), str(sumber), str(author), str(url))
                                         no += 1
                                 else:
                                     for s in anu:
                                         syit = s
                                         sumber = syit['source']['name']
                                         author = syit['author']
                                         judul = syit['title']
                                         url = syit['url']
                                         ret_ += "\n\n{}. Judul : {}\n    Sumber : {}\n    Penulis : {}\n    Link : {}".format(str(no), str(judul), str(sumber), str(author), str(url))
                                         no += 1
                                 client.sendMessage(to, str(ret_))
                             except:
                                 client.sendMessage(to, "Top news Not Found !")
                        elif cmd.startswith("à¸à¸²à¸¡ "):
                            kata = cmd.replace("asking", "")
                            sch = kata.replace(" ","+")
                            with _session as web:
                                urlz = "http://lmgtfy.com/?q={}".format(str(sch))
                                r = _session.get("http://tiny-url.info/api/v1/create?apikey=A942F93B8B88C698786A&provider=cut_by&format=json&url={}".format(str(urlz)))
                                data = r.text
                                data = json.loads(data)
                                url = data["shorturl"]
                                ret_ = "ãAskã"
                                ret_ += "\n\nLink : {}".format(str(url))
                                client.sendMessage(to, str(ret_))
                        elif cmd.startswith("à¸à¸²à¸à¸¹à¸ "):
                            judul = cmd.replace("à¸à¸²à¸à¸¹à¸", "")
                            with _session as web:
                                try:
                                    r = web.get("https://kitsu.io/api/edge/anime?filter[text]={}".format(str(judul)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["data"][0]
                                    title = anu["attributes"]["titles"]["en_jp"]
                                    synopsis = anu["attributes"]["synopsis"]
                                    id = anu["id"]
                                    link = anu["links"]["self"]
                                    ret_ = "ãAbout Animeã"
                                    ret_ += "\n\nTitle : {}\nSynopsis : {}\nId : {}\nLink : {}".format(str(title), str(synopsis), str(id), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "No result found")
                        elif cmd.startswith("searchanime "):
                            kata = cmd.replace("searchanime", "")
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]["anime"][0]
                                    title = anu['title']
                                    link = anu['link']
                                    ret_ = "ãAnimeã"
                                    ret_ += "\n\nTitle : {}\nLink : {}".format(str(title), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "No result found")
                        elif cmd.startswith("searchmanga "):
                            kata = cmd.replace("searchmanga", "")
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]["manga"][0]
                                    title = anu['title']
                                    link = anu['link']
                                    ret_ = "ãMangaã"
                                    ret_ += "\n\nTitle : {}\nLink : {}".format(str(title), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "No result found")
                        elif cmd.startswith("searchcharacter "):
                            kata = cmd.replace("searchcharacter", "")
                            with _session as web:
                                try:
                                    r = web.get("http://ariapi.herokuapp.com/api/anime/search?q={}".format(urllib.parse.quote(kata)))
                                    data = r.text
                                    data = json.loads(data)
                                    anu = data["result"]["character"][0]
                                    title = anu['title']
                                    link = anu['link']
                                    ret_ = "ãCharacterã"
                                    ret_ += "\n\nTitle : {}\nLink : {}".format(str(title), str(link))
                                    client.sendMessage(to, str(ret_))
                                except:
                                    client.sendMessage(to, "No result found")
                        elif cmd.startswith("gif "):
                            proses = text.split(" ")
                            urutan = text.replace(proses[0] + " ","")
                            count = urutan.split("|")
                            search = str(count[0])
                            r = requests.get("https://api.tenor.com/v1/search?key=PVS5D2UHR0EV&limit=10&q="+str(search))
                            data = json.loads(r.text)
                            if len(count) == 1:
                                no = 0
                                hasil = "Search Gif\n"
                                for aa in data["results"]:
                                    no += 1
                                    hasil += "\n" + str(no) + ". " + str(aa["title"])
                                    ret_ = "\n\nGif {} | num\nFor view detail video".format(str(search))
                                client.sendMessage(to,hasil+ret_)
                            elif len(count) == 2:
                                try:
                                    num = int(count[1])
                                    b = data["results"][num - 1]
                                    c = str(b["id"])
                                    hasil = "Informasi gif ID "+str(c)
                                    hasil += "\n"
                                    client.sendMessage(msg.to,hasil)
                                    dl = str(b["media"][0]["loopedmp4"]["url"])
                                    client.sendVideoWithURL(msg.to,dl)
                                except Exception as e:
                                    client.sendMessage(to," "+str(e))                                              
                        elif cmd.startswith("imageart "):
                            try:                                   
                                search = cmd.replace("imageart ","")
                                r = requests.get("https://xeonwz.herokuapp.com/images/deviantart.api?q={}".format(search))
                                data = r.text
                                data = json.loads(data)
                                if data["content"] != []:
                                    items = data["content"]
                                    path = random.choice(items)
                                    a = items.index(path)
                                    b = len(items)
                                    client.sendImageWithURL(to, str(path))
                                    client.sendMessage(to,"Art #%s from #%s." %(str(a),str(b)))
                                    log.info("Art #%s from #%s." %(str(a),str(b)))
                            except Exception as error:
                                 log.info(error)
#============================================================================================================
#=====================================================[]=======================================================
#==============================================================================================================
                if msg.contentType == 13:
                    if settings["wblacklist"] == True:
                        if msg.contentMetadata["mid"] in settings["blacklist"]:
                            client.sendMessage(to,"ãDoneã")
                            settings["wblacklist"] = False
                        else:
                            settings["blacklist"][msg.contentMetadata["mid"]] = True
                            settings["wblacklist"] = False
                            client.sendMessage(to,"ãDoneã")
                    elif settings["dblacklist"] == True:
                        if msg.contentMetadata["mid"] in settings["blacklist"]:
                            del settings["blacklist"][msg.contentMetadata["mid"]]
                            client.sendMessage(to,"ãDoneã")
                            settings["dblacklist"] = False
                        else:
                            settings["dblacklist"] = False
                            client.sendMessage(to,"ãDoneã")
                if msg.contentType == 13:
                    if settings["wwhitelist"] == True:
                        if msg.contentMetadata["mid"] in settings["whitelist"]:
                            client.sendMessage(to,"ãDoneã")
                            settings["wwhitelist"] = False
                        else:
                            settings["whitelist"][msg.contentMetadata["mid"]] = True
                            settings["wwhitelist"] = False
                            client.sendMessage(to,"ãDoneã")
                    elif settings["dwhitelist"] == True:
                        if msg.contentMetadata["mid"] in settings["whitelist"]:
                            del settings["whitelist"][msg.contentMetadata["mid"]]
                            client.sendMessage(to,"ãDoneã")
                            settings["dwhitelist"] = False
                        else:
                            settings["dwhitelist"] = False
                            client.sendMessage(to,"ãDoneã")
#==============================================================================================================
#=====================================================[]=======================================================
#==============================================================================================================
                if msg.contentType == 13:
                    if settings["checkContact"] == True:
                        msg.contentType = 0
                        client.sendMessage(msg.to,msg.contentMetadata["mid"])
                        if 'displayName' in msg.contentMetadata:
                            contact = client.getContact(msg.contentMetadata["mid"])
                            try:
                                cu = client.getProfileCoverURL(msg.contentMetadata["mid"])
                            except:
                                cu = ""
                            client.sendMessage(msg.to,"ãDisplayNameã:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                        else:
                            contact = client.getContact(msg.contentMetadata["mid"])
                            try:
                                cu = client.getProfileCoverURL(msg.contentMetadata["mid"])
                            except:
                                cu = ""
                            if settings["server"] == "VPS":
                                client.sendMessage(msg.to, "ãDisplayNameã:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                                client.sendImageWithURL(msg.to, "http://dl.profile.line-cdn.net/" + contact.pictureStatus)
                                client.sendImageWithURL(msg.to, str(cu))
#==============================================================================================================
#=====================================================[]=======================================================
#==============================================================================================================
                    for image in images:
                        if text.lower() == image:
                            client.sendImage(to, images[image])
                    for sticker in stickers:
                        if text.lower() == sticker:
                            sid = stickers[sticker]["STKID"]
                            spkg = stickers[sticker]["STKPKGID"]
                            sver = stickers[sticker]["STKVER"]
                            sendSticker(to, sver, spkg, sid)
                if msg.contentType == 1:
                    if settings["changePicture"] == True:
                        path = client.downloadObjectMsg(msg_id)
                        settings["changePicture"] = False
                        client.updateProfilePicture(path)
                        client.sendMessage(to, "Update profile picture Succes")
                    if msg.toType == 2:
                        if to in settings["changeGroupPicture"]:
                            path = client.downloadObjectMsg(msg_id)
                            settings["changeGroupPicture"].remove(to)
                            client.updateGroupPicture(to, path)
                            client.sendMessage(to, "Update group picture Succes")
                elif msg.contentType == 2:
                    if settings['changeProfileVideo']['status'] == True and sender == clientMID:
                        path = client.downloadObjectMsg(msg_id)
                        if settings['changeProfileVideo']['stage'] == 1:
                            settings['changeProfileVideo']['video'] = path
                            client.sendMessage(to, "Send a pict to change change dual")
                            settings['changeProfileVideo']['stage'] = 2
                        elif settings['changeProfileVideo']['stage'] == 2:
                            settings['changeProfileVideo']['video'] = path
                            changeProfileVideo(to)
                elif msg.contentType in [1,2]:
                    if sender in clientMID:
                        client.sendMessage(to, str(msg))
#==============================================================================================================
#=====================================================[]=======================================================
#==============================================================================================================                        
        if op.type == 25:
#            if settings ["mutebot2"] == True:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != client.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
#========================================================================                    
                if msg.contentType == 7:
                    if settings["messageSticker"]["addStatus"] == True:
                        name = settings["messageSticker"]["addName"]
                        if name != None and name in settings["messageSticker"]["listSticker"]:
                            settings["messageSticker"]["listSticker"][name] = {
                                "STKID": msg.contentMetadata["STKID"],
                                "STKVER": msg.contentMetadata["STKVER"],
                                "STKPKGID": msg.contentMetadata["STKPKGID"]
                            }
                            client.sendMessage(to, "Success Added " + name)
                        settings["messageSticker"]["addStatus"] = False
                        settings["messageSticker"]["addName"] = None
                    if settings["addSticker"]["status"] == True:
                        stickers[settings["addSticker"]["name"]]["STKVER"] = msg.contentMetadata["STKVER"]
                        stickers[settings["addSticker"]["name"]]["STKID"] = msg.contentMetadata["STKID"]
                        stickers[settings["addSticker"]["name"]]["STKPKGID"] = msg.contentMetadata["STKPKGID"]
                        f = codecs.open('sticker.json','w','utf-8')
                        json.dump(stickers, f, sort_keys=True, indent=4, ensure_ascii=False)
                        client.sendMessage(to, "Success Added sticker {}".format(str(settings["addSticker"]["name"])))
                        settings["addSticker"]["status"] = False
                        settings["addSticker"]["name"] = ""
                        
        if op.type == 26:
#            if settings ["mutebot2"] == True:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != client.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                        contact = client.getContact(sender)
                        txt = '[%s] %s' % (contact.displayName, text)
                        client.log(txt)
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    if msg.contentType == 7:
                        stk_id = msg.contentMetadata['STKID']
                        stk_ver = msg.contentMetadata['STKVER']
                        pkg_id = msg.contentMetadata['STKPKGID']
                        ret_ = "Sticker Info"
                        ret_ += "\nSTICKER ID : {}".format(stk_id)
                        ret_ += "\nSTICKER PACKAGES ID : {}".format(pkg_id)
                        ret_ += "\nSTICKER VERSION : {}".format(stk_ver)
                        client.sendMessage(to, text=None, contentMetadata={'STKID':'107', 'STKVER':'100', 'STKPKGID':'1'}, contentType=7)
                    elif msg.contentType == 1:
                        client.sendMessage(to, text=None, contentMetadata={"STKID": "190", "STKVER": "100", "STKPKGID": "3"}, contentType=7)
                    else:
                        if text is not None:
                            txt = text
                            client.sendMessage(msg.to,txt)
                elif msg.contentType == 7:
                    if settings["checkSticker"] == True:
                        try:
                            stk_id = msg.contentMetadata['STKID']
                            stk_ver = msg.contentMetadata['STKVER']
                            pkg_id = msg.contentMetadata['STKPKGID']
                            ret_ = "ã Check Sticker ã\n"
                            ret_ += "\nSTKID : {}".format(stk_id)
                            ret_ += "\nSTKPKGID : {}".format(pkg_id)
                            ret_ += "\nSTKVER : {}".format(stk_ver)
                            ret_ += "\nLINK : line://shop/detail/{}".format(pkg_id)
                            print(msg)
                            client.sendImageWithURL(to, "http://dl.stickershop.line.naver.jp/products/0/0/"+msg.contentMetadata["STKVER"]+"/"+msg.contentMetadata["STKPKGID"]+"/WindowsPhone/stickers/"+msg.contentMetadata["STKID"]+".png")
                            client.sendMessage(to, str(ret_))                            
                        except Exception as error:
                            client.sendMessage(to, str(error))
                    if msg.contentType == 7:
                        if settings["sticker"]:
                            client.sendMessage(to,"do not send stickers, your stickers are cheap :v")
                            client.kickoutFromGroup(msg.to,[sender])
                if msg.contentType == 0:
                    if msg.toType == 0:
                        if settings["autoRead"] == True:
                            client.sendChatChecked(to, msg_id)
                    elif msg.toType == 2:
                        if settings["autoRead"] == True:
                            client.sendChatChecked(to, msg_id)
                #if msg.text in ["à¹à¸à¸¥à¹à¸à¸£"]:
                 #   client.sendText(msg.to,"ððà¹à¸à¸¥à¸à¸­à¸ðð\nðÅ¤á»ÃÎ Ð¶ Î²Ç¾Å¦ðà¸¿Ç¾Â¥ð")                
#==============================================================================================================
#=====================================================[]=======================================================
#==============================================================================================================
        if op.type == 32:
            if op.param1 in settings["pcancel"]:
                if op.param2 not in Bots or op.param2 not in settings["whitelist"]:
                    group = client.getGroup(op.param1)
                    group.preventedJoinByTicket = True
                    client.updateGroup(group)
                    client.kickoutFromGroup(op.param1,[op.param2])
                    client.sendMessage(op.param1, text=None, contentMetadata={'mid': op.param2}, contentType=13)
#==============================================================================================================
    #    if op.type == 65:
#                try:
   #                 at = op.param1
  #                  msg_id = op.param2
    #                if msg_id in msg_dict:
           #####             if msg_dict[msg_id]["from"] not in clientMID:
   #                         client.sendMessage(at,"Sent Message Cancelled\n\nSender :\n%s\nSentAt :\n%s\nDetail :\n%s"%(client.getContact(msg_dict[msg_id]["from"]).displayName,dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"])),msg_dict[msg_id]["text"]))
    #                    else:
     #                       client.sendMessage(to, str(ret_))
    #                    del msg_dict[msg_id]
    #                else:
 #                       client.sendMessage(at,"SentMessage cancelled\nBut I didn't have log data.Sorry > <")
   #     ##        except Exception as e:
 #                   print(e)
        if op.type == 65:
            print ("[ 65 ] NOTIFIED DESTROY MESSAGE")
            if settings["unsendMessage"] == True:
                at = op.param1
                msg_id = op.param2
                if msg_id in msg_dict:
                    ah = time.time()
                    ikkeh = client.getContact(msg_dict[msg_id]["from"])
                    if "text" in msg_dict[msg_id]:
                        waktumsg = ah - msg_dict[msg_id]["waktu"]
                        waktumsg = format_timespan(waktumsg)
                        rat_ = "\nSend At :\n{} ago".format(waktumsg)
                        rat_ += "\nText :\n{}".format(msg_dict[msg_id]["text"])
                        sendMention(at, ikkeh.mid, " ** Resend Message **\n\nMaker :\n", str(rat_))
                        del msg_dict[msg_id]
                    else:
                        if "image" in msg_dict[msg_id]:
                            waktumsg = ah - msg_dict[msg_id]["waktu"]
                            waktumsg = format_timespan(waktumsg)
                            rat_ = "\nSend At :\n{} ago".format(waktumsg)
                            rat_ += "\nImage :\nBelow"
                            sendMention(at, ikkeh.mid, "** Resend Message **\n\nMaker :\n", str(rat_))
                            client.sendImage(at, msg_dict[msg_id]["image"])
                            del msg_dict[msg_id]
                        else:
                            if "video" in msg_dict[msg_id]:
                                waktumsg = ah - msg_dict[msg_id]["waktu"]
                                waktumsg = format_timespan(waktumsg)
                                rat_ = "\nSend At :\n{} ago".format(waktumsg)
                                rat_ += "\nVideo :\nBelow"
                                sendMention(at, ikkeh.mid, "** Resend Message **\n\nMaker :\n", str(rat_))
                                client.sendVideo(at, msg_dict[msg_id]["video"])
                                del msg_dict[msg_id]
                            else:
                                if "audio" in msg_dict[msg_id]:
                                    waktumsg = ah - msg_dict[msg_id]["waktu"]
                                    waktumsg = format_timespan(waktumsg)
                                    rat_ = "\nSend At :\n{} ago".format(waktumsg)
                                    rat_ += "\nAudio :\nBelow"
                                    sendMention(at, ikkeh.mid, "** Resend Message **\n\nMaker :\n", str(rat_))
                                    client.sendAudio(at, msg_dict[msg_id]["audio"])
                                    del msg_dict[msg_id]
                                else:
                                    if "sticker" in msg_dict[msg_id]:
                                        waktumsg = ah - msg_dict[msg_id]["waktu"]
                                        waktumsg = format_timespan(waktumsg)
                                        rat_ = "\nSend At :\n{} ago".format(waktumsg)
                                        rat_ += "\nSticker :\nBelow"
                                        sendMention(at, ikkeh.mid, " ** Resend Message **\n\nMaker :\n", str(rat_))
                                        client.sendImageWithURL(at, msg_dict[msg_id]["sticker"])
                                        del msg_dict[msg_id]
                                    else:
                                        if "mid" in msg_dict[msg_id]:
                                            waktumsg = ah - msg_dict[msg_id]["waktu"]
                                            waktumsg = format_timespan(waktumsg)
                                            rat_ = "\nSend At :\n~ {} ago".format(waktumsg)
                                            rat_ += "\nContact :\nBelow"
                                            sendMention(at, ikkeh.mid, "** Resend Message **\n\nMaker :\n", str(rat_))
                                            client.sendContact(at, msg_dict[msg_id]["mid"])
                                            del msg_dict[msg_id]
                                        else:
                                            if "lokasi" in msg_dict[msg_id]:
                                                waktumsg = ah - msg_dict[msg_id]["waktu"]
                                                waktumsg = format_timespan(waktumsg)
                                                rat_ = "\nSend At :\n{} ago".format(waktumsg)
                                                rat_ += "\nLocate :\nBelow"
                                                sendMention(at, ikkeh.mid, "** Resend Message **\n\nMaker :\n", str(rat_))
                                                client.sendLocation(at, msg_dict[msg_id]["lokasi"])
                                                del msg_dict[msg_id]
                                            else:
                                                if "file" in msg_dict[msg_id]:
                                                    waktumsg = ah - msg_dict[msg_id]["waktu"]
                                                    waktumsg = format_timespan(waktumsg)
                                                    rat_ = "\nSend At :\n{} ago".format(waktumsg)
                                                    rat_ += "\nFile :\nBelow"
                                                    sendMention(at, ikkeh.mid, "** Resend Message **\n\nMaker :\n", str(rat_))
                                                    client.sendFile(at, msg_dict[msg_id]["file"])
                                                    del msg_dict[msg_id]
                else:
                    client.sendMessage(at, "Unsend Message Detected\n\nMessage not in log")
        if op.type == 55:
                try:
                    if sider['cyduk'][op.param1]==True:
                        if op.param1 in sider['point']:
                            Name = client.getContact(op.param2).displayName
                            if Name in sider['sidermem'][op.param1]:
                                pass
                            else:
                                sider['sidermem'][op.param1] += "\n~ " + Name
                                zxn=["Jangan sider terus ","Jangan sider ","Halo ayo kita ngobrol ","Turun kak ikut chat ","Sider mulu ","sider tak doakan jones ","Ciyyee yang lagi ngintip ","Hai Kang ngintip ","Jangan sider mulu dong kk "]
                                #client.sendMessage(op.param1, str(random.choice(zxn))+' '+Name)                                                              
                                dhil(op.param1,[op.param2])
                        else:
                            pass
                    else:
                        pass
                except:
                    pass
        else:
            pass
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            if op.param1 in settings["getReader"] and op.param2 not in settings["getReader"][op.param1]:
                msgSticker = settings["messageSticker"]["listSticker"]["readerSticker"]
                if msgSticker != None:
                    sid = msgSticker["STKID"]
                    spkg = msgSticker["STKPKGID"]
                    sver = msgSticker["STKVER"]
                    sendSticker(op.param1, sver, spkg, sid)
                if "@!" in settings["readerPesan"]:
                    msg = settings["readerPesan"].split("@!")
                    sendMention(op.param1, op.param2, msg[0], msg[1])
                else:
                    sendMention(op.param1, op.param2, "à¸à¹à¸°à¹à¸­à¹", settings["readerPesan"])
                settings["getReader"][op.param1].append(op.param2)   
#==============================================================================================================
        if op.type == 17:
            if op.param1 in welcomemsg:
                ginfo = client.getGroup(op.param1)
                contact = client.getContact(op.param2)
                ppnh = ["Selamatdatang ", "Halooo welcome kak ","Asek Selamat Datang"]
                ppsd = ["Jangan lupa jalan ke note","Jangan lupa cari tikungan ","Semoga Dapet Jodoh"]
                path = "http://dl.profile.line.naver.jp/" + contact.pictureStatus
                client.sendImageWithURL(op.param1,path)
                sendMention(op.param1,op.param2,client(ppnh)," di " + ginfo.name +"N" + client(ppsd) +":)")
                print ("[Notif] Pesan Sambutan Succes")     

        if op.type == 55:
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================================================
def cium(to, nama):
    aa = ""
    bb = ""
    strt = int(0)
    akh = int(0)
    nm = nama
    myid = "u4862fe4b182b2fd194a3108e2f3662e8"
    if myid in nm:    
      nm.remove(myid)
    #print nm
    for mm in nm:
      akh = akh + 6
      aa += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(mm)+"},"""
      strt = strt + 7
      akh = akh + 1
      bb += "@FUCK \n"
    aa = (aa[:int(len(aa)-1)])
    text = bb
    try:
       client.sendMessage(to, text, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
       print(error)
#==============================================================================================================

#=====================================================[]=======================================================
def sendMention(to, mid, firstmessage, lastmessage):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@x "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        client.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))
#===============================================
def khieMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
#==============================================================================================================
def dhil(to, mid):
    try:
        arrData = ""
        group = client.getGroup(to)
        textx = ""+ str(settings["anu"]) +" "
        arr = []
        no = 1
        for i in mid:
            mention = "@Rh "
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
            if int(no) < int(len(mid)):
                no += 1
                textx += "   â¢ "
            else:
                textx += " "+ str(settings["anu2"]) +""
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))
#==============================================================================================================
def mentionMembers(to, mid):
    try:
        group = client.getGroup(to)
        mids = [mem.mid for mem in group.members]
        jml = len(mids)
        arrData = ""
        if mid[0] == mids[0]:
            textx = "à¸ªà¸¡à¸²à¸à¸´à¸ {} à¸à¸\n\n".format(str(jml))
        else:
            textx = ""
        arr = []
        for i in mid:
            no = mids.index(i) + 1
            textx += "{}. ".format(str(no))
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
        if no == jml:
            textx += ""
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))
def samMention(to, mid, firstmessage, lastmessage):
    try:
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@sam "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        client.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))
#==============================================================================================================
def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in settings['readPoint']:
                    if msg._from in settings["ROM"][msg.to]:
                        del settings["ROM"][msg.to][msg._from]
                else:
                    pass
            except:
                pass
        else:
            pass
          
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print(error)
        print("\n\nRECEIVE_MESSAGE\n\n")
        return
#==============================================================================================================
def atend():
    with open("Log_data.json","w",encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False, indent=4,separators=(',', ': '))
atexit.register(atend)
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    time.sleep(10)
    python = sys.executable
    os.execl(python, python, *sys.argv)
def autoRestart():
    if time.time() - botStart > int(settings["timeRestart"]):
        backupData()
        time.sleep(5)
        restartBot()
#==============================================================================================================
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = stickers
        f = codecs.open('sticker.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = images
        f = codecs.open('image.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
#==============================================================================================================

while True:
    try:
        delExpire()
        delete_log()
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
