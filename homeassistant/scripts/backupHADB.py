#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import required modules
import sys
import os
import datetime
import sqlite3
import dropbox
import smtplib

# Definition of functions for uploading the database backup to Dropbox
class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a single file <150MB to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            print(dbx.files_upload(f.read(), file_to))

    def upload_large_file(self, file_from, file_to, file_size, chunk_size):
        """upload a file >150MB to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            upload_session_start_result = dbx.files_upload_session_start(f.read(chunk_size))
            cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                               offset=f.tell())
            commit = dropbox.files.CommitInfo(path=file_to, mute=False)
            while f.tell() < file_size:
                if ((file_size - f.tell()) <= chunk_size):
                    print(dbx.files_upload_session_finish(f.read(chunk_size), cursor, commit))
                else:
                    dbx.files_upload_session_append(f.read(chunk_size), cursor.session_id, cursor.offset)
                    cursor.offset = f.tell()

class GMailSender:
    def __init__(self):
        self.user = "[REPLACE WITH MAILADDRESS]"
        self.pw = "[REPLACE WITH PASSWORD]"
        self.recipients = ["[REPLACE WITH RECIPIENT1]", "[REPLACE WITH RECIPIENT2]"]
    
    def sendGMail(self, email):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.user, self.pw)
        server.sendmail(self.user, self.recipients, email)
        server.close()


try:
    pathToLog = "/home/homeassistant/.homeassistant/scripts/backupHADB.log"

    # Create a timestamp
    now = datetime.datetime.now()
    timestamp = now.strftime("%d%m%Y-%H%M%S")
     
    print("backupHADB.py called on: " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    cmdWriteToLog = "echo " + "backupHADB.py called on: " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + " >> " + pathToLog
    os.system(cmdWriteToLog)
   
    # Start the script run 
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "START: Regular backup, upload and cleaning of the Home Assistant DB")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "START: Regular backup, upload and cleaning of the Home Assistant DB" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    # 1. Stop the Home Assistant service
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "1. Stopping the Home Assistant service")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "1. Stopping the Home Assistant service" + "  >> " +  pathToLog
    os.system(cmdWriteToLog)

    cmdStopHA = "sudo systemctl stop home-assistant@homeassistant.service"
    os.system(cmdStopHA)

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully stopped the Home Assistant service")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully stopped the Home Assistant service" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    # Define the backup output name
    backupName = timestamp + "_" + "HA_DB_BACKUP.tar.gz"
    fullBackupPath  = "/home/homeassistant/.homeassistant/" + backupName

    # 2. Create a Home Assistant database backup (.tar.gz)
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "2. Creating the Home Assistant DB backup")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "2. Creating the Home Assistant DB backup" + " >> " + pathToLog
    os.system(cmdWriteToLog)    

    cmdBackup = "tar -zcvf " + fullBackupPath + " /home/homeassistant/.homeassistant/home-assistant_v2.db"
    os.system(cmdBackup)

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully created the Home Assistant DB backup")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully created the Home Assistant DB backup" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    # 3.  Upload the Home Assistant database backup to Dropbox
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "3. Uploading the Home Assistant DB backup to Dropbox")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "3. Uploading the Home Assistant DB backup to Dropbox" + " >> " + pathToLog    
    os.system(cmdWriteToLog)

    access_token = '[REPLACE WITH ACCESS TOKEN]'
    transferData = TransferData(access_token)

    file_from = fullBackupPath
    file_to = '/DB_Backups/' + backupName  # The full path to upload the file to, including the file name

    file_size = os.path.getsize(file_from)
    chunk_size = 134217728

    if file_size <= chunk_size:
        transferData.upload_file(file_from, file_to)
    else:
        transferData.upload_large_file(file_from, file_to, file_size, chunk_size)

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully uploaded the Home Assistant DB backup to Dropbox")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully uploaded the Home Assistant DB backup to Dropbox" + " >> " + pathToLog
    os.system(cmdWriteToLog)    

    # 4. Delete all (!) records from the original Home Assistant database and optimize its space consumption
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "4. Deleting all records from the original Home Assistant DB and optimizing its space consumption")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "4. Deleting all records from the original Home Assistant DB and optimizing its space consumption" + " >> " + pathToLog
    os.system(cmdWriteToLog)
   
    connection = sqlite3.connect("/home/homeassistant/.homeassistant/home-assistant_v2.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM states;""")
    connection.commit()

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully deleted all records from the Home Assistant DB")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully deleted all records from the Home Assistant DB" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    cursor.execute("""VACUUM;""")
    connection.commit()
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully optimized the space consumption of the Home Assistant DB")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully optimized the space consumption of the Home Assistant DB" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    connection.close()

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully finished all database operations")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully finished all database operations" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    # 5. Start the Home Assistant service
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "5. Starting the Home Assistant service")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "5. Starting the Home Assistant service" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    cmdStartHA = "sudo systemctl start home-assistant@homeassistant.service"
    os.system(cmdStartHA)

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully started the Home Assistant service")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully started the Home Assistant service" + " >> " + pathToLog
    os.system(cmdWriteToLog)
 
    # 6. Send an email signalling successful completion of upload
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "6. Sending email notification")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "6. Sending email notification" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    gMailSender = GMailSender()
    subject = "Home Assistant DB Backup Successful"
    text = "Hallo,\n\ndas Backup der Home Assistant Datenbank ist erfolgreich durchgelaufen. Sie finden das aktuelle Backup unter: https://www.dropbox.com/sh/iq57xdtff0tv20a/AABvsOUZXgAhzKisoGFB0BLaa?dl=0.\n\n- Das Digital HHZ Team"
    gMailSender.sendGMail('Subject: {}\n\n{}'.format(subject, text))

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully sent email notification.")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "Successfully sent email notification" + " >> " + pathToLog
    os.system(cmdWriteToLog)

    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "END: Successfully finished the regular backup, upload and cleaning of the Home Assistant DB")
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "END: Successfully finished the regular backup, upload and cleaning of the Home Assistant DB" + " >> " + pathToLog
    os.system(cmdWriteToLog)

except Exception as e:
    print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + "An error occurred: "+e)
    cmdWriteToLog = "echo " + datetime.datetime.now().strftime("%H:%M:%S") + " - " + "An error occurred: " + e
    os.system(cmdWriteToLog) 
    gMailSender = GMailSender()
    subject = "Home Assistant DB Backup Failed"
    text = "Hallo,\n\ndas Backup der Home Assistant Datenbank ist fehlgeschlagen.\nDas Skript hat folgenden Fehler geworfen: "+e+"\n\n- Das Digital HHZ Team"
    gMailSender.sendGMail('Subject: {}\n\n{}'.format(subject, text))
    print("Email alert sent.")
