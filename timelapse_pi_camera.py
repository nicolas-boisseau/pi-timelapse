#!/usr/bin/python

# https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f


import time
import os
from datetime import datetime
from picamera2 import Picamera2
from ftplib import FTP_TLS


class TimelapsePiCamera:
    """Abstraction of Pi Camera, in order to make regular snapshots and build a timelapse video"""

    intervalInSeconds = 60

    def __init__(self, intervalInSeconds):
        self.intervalInSeconds = intervalInSeconds

        print("Initializing PiCamera2...")
        self.picam2 = Picamera2()
        self.picam2.configure("still")
        self.picam2.start()
        self.picam2.autofocus_cycle()
        time.sleep(1)
        self.picam2.set_controls({"AeEnable": True, "AwbEnable": True, "FrameRate": 1.0})
        time.sleep(1)
        print("DONE !")

        print("Initializing FTP config from ENV")
        self.ftp_host = os.environ['FTP_HOST']
        self.ftp_user = os.environ['FTP_USER']
        self.ftp_password = os.environ['FTP_PASSWORD']
        self.ftp_path = os.environ['FTP_PATH']

    def start(self):
        print("Start loop...")
        while True:
            print("Shooting...")
            self.shoot()
            print("Done !")

            time.sleep(self.intervalInSeconds)

    def getFilename(self):
        now = datetime.now()
        nowStr = now.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        filename = "/home/pi/pi-timelapse/snapshots/timelapse_{}.jpg".format(nowStr)
        return filename

    def saveToFtp(self, filename):
        # note : be sure that the host DNS resolution is OK ou add it manually to /etc/hosts
        ftp = FTP_TLS(self.ftp_host)
        ftp.login(self.ftp_user, self.ftp_password)
        ftp.cwd(self.ftp_path)
        remoteFileName = filename.split("/")[-1]
        ftp.storbinary("STOR " + remoteFileName, open(filename, 'rb'))
        ftp.quit()

    def shoot(self):
        filename = self.getFilename()

        self.picam2.autofocus_cycle()
        capture_request = self.picam2.capture_request()
        capture_request.save("main", filename)
        capture_request.release()
        print("Saving to file " + filename)

        print("Try to upload to FTP...")
        try:
            self.saveToFtp(filename)
            print("DONE!")
            # remove the local file only when operation is successful
            os.remove(filename)
        except Exception as ex:
            print("FAILED with error :")
            print(ex)


if __name__ == "__main__":
    cam = TimelapsePiCamera(30)
    cam.start()
    # cam.shoot()
