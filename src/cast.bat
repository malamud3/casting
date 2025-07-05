@echo off
:: If a serial (%1) was supplied (e.g. 192.168.x.x:5555) mirror that device;
:: otherwise fall back to scrcpy’s default behaviour (first device in list).

if "%~1"=="" (
    scrcpy --render-driver=opengl ^
           --crop 1600:900:2017:510 ^
           --no-audio ^
           -b4M ^
           --max-size 1024 ^
           --video-codec=h264 ^
           --video-encoder=OMX.qcom.video.encoder.avc ^
           -n
) else (
    scrcpy -s %1 ^
           --render-driver=opengl ^
           --crop 1600:900:2017:510 ^
           --no-audio ^
           -b4M ^
           --max-size 1024 ^
           --video-codec=h264 ^
           --video-encoder=OMX.qcom.video.encoder.avc ^
           -n
)
