[Setting up the Pi](#setting-up-the-pi)


# Setting up the Pi
The following are the steps we used to set up our Raspberry 4 Model B with 4Gb RAM.  

- Format the micro SD to `MS-DOS (FAT32)`.

- Download NOOBS, the full version, not the lite version, from `https://downloads.raspberrypi.org`. Uncompress the downloaded file and save the contents to the SD card using `unzip NOOBS_v3_8_1.zip -d path_to_sd_card`.  
 
- Connect the Pi to a screen, mouse, and keyboard, then plug it in. The lights on the Pi started to flash and the screen lit up shortly afterwards. We set up the WIFI, and then installed *Raspberry Pi OS Full (32-bit) with desktop and recommended software*. The installation took less than 10 minutes. Then the Pi rebooted into the new OS automatically. We followed the on-screen instructions to choose a location and set up an account. Updating the OS took a while, but the process went smoothly, requiring no user input.


- Create SSH key pair
  - `ssh-keygen -t ed25519 -C "email@server.com"`, enter a passphrase and save file to the default location.
  - Add the SSH key to `ssh-agent` by using 
    ```
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    ```
  - Add SSH key to Github account.