# My Photo Frame 

I built this to operate my DIY digital photo frame. It's built on a Raspberry Pi model 3 B+ and a 6-inch e-Paper HAT from Waveshare.

NOTE: This is the second version, the original one was based on a slighly modified C application. Some leftover code is still in the repo, cleanup is in progress. The google photos integration doesn't work yet.

# Dependencies
I use the following python module to communicate with the e-paper device:
https://github.com/GregDMeyer/IT8951

# Enable auto-start

```
sudo cp ~/myphotoframe/slideshow.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable slideshow.service
```

To check status run `systemctl status slideshow.service`.

To temporarily stop the service (e.g., while developing) run `sudo systemctl stop slideshow.service` and then to restart `sudo systemctl start slideshow.service`.


# Troubleshooting
Make sure that SPI is enabled in `raspi-config`.

If anything goes wrong you can restart the SPI
```
sudo dtparam spi=off
sudo dtparam spi=on
```
