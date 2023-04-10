# PI-timelapse

This project aims to take photos automatically every x seconds with the raspberry camera and the PiCamera2 library. 
Then, it sends  the photos to a backend FTP which compute a video with ffmpeg and output a mp4 video. 

Required stuff :
- 1 raspberry pi zero (but it should work with any raspberry pi supporting camera)
- 1 pi camera v3 (but should work with previous models)
- 1 ribbon cable for pi zero (only with pi zero)
- 3D-printed camera support (TODO : link to thingiverse)
- 3D-printed raspberry pi zero box (TODO: link to thingiverse)
- FTP server (to receive snapshots)
- linux or docker based server supporting ffmpeg (to compute video)


# Sources / inspiration
[magpi.cc/timelapsepy](https://magpi.cc/timelapsepy)

