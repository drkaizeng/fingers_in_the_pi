## Setting up the Pi
- Format the micro SD to `MS-DOS (FAT32)`
- Download NOOBS, the full version, not the lite version, from `https://downloads.raspberrypi.org`. Uncompress the downloaded file and the contents to the SD card using `unzip NOOBS_v3_8_1.zip -d path_to_sd_card`.




- Create SSH key pair
  - `ssh-keygen -t ed25519 -C "email@server.com"`, enter a passphrase and save file to the default location.
  - Add the SSH key to `ssh-agent` by using 
    ```
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    ```
  - Add SSH key to Github account.