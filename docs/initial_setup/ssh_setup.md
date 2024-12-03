# Enabling access via SSH
Although our Pi is a powerful little computer, we prefer to do most of our work remotely. This way, we have easy access to the files and tools on our Mac, which makes development work go more smoothly. Furthermore, we can let the Pi boot into the CLI (i.e., the command line, without starting a desktop), which saves computing power. 

- Enable SSH
  - Boot into the Pi OS desktop. In "Preferences (access via top-right raspberry icon) > Paspberry Pi Configuration > Interfaces", enable "SSH". Click "OK" to confirm.
  - If the installed OS has no desktop, then use `sudo apt install openssh-server` to install the server, `sudo service ssh start` to start the server, and `sudo systemctl enable ssh` to ensure that the service starts automatically on start-up.

- Find out the IP address by issuing `ip addr` in the terminal. We use the WIFI. So the IP can be found in the section about `wlan0`. If you use an ethernet cable, then focus on `eth0`. On another compute on the same network (a Mac in our case), issue `ssh $ip_addr`, where `$ip_addr` is the value returned by the previous step, and follow the on-screen instructions to log in.


## SSH key pair on the Mac
To avoid having to type password to log in via SSH everytime, we created an SSH key pair on the Mac (identical steps of Linux machines). These steps are all done in a terminal.

- Issue `ssh-keygen -t ed25519 -C "an_informative_comment"`, enter a passphrase and save file to the default location. (NB: it is easier to leave passphrase blank to avoid having to enter password or setting up a key chain)

- Add the SSH key to `ssh-agent` by using 
  ```
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
  ```

- Add the public key to the Pi by `ssh-copy-id user_name@ip_addr`, where user_name should be replaced by the actual user name of the Pi, and ip_addr is the IP address of the Pi. We should now be able to use `ssh user_name@ip_addr` without entering the Pi's password.

- If the home broadband router permits, set it up so that it gives the Pi the same IP address everytime. Then on the non-Pi machine add `ip_addr rpi` to `/etc/hosts`, where `rpi` can be replaced by any other easy-to-remember name (this step requires `sudo` privilege). We can log in just using `ssh user_name@rpi`.

- To make things even easier, on the non-Pi machine, add `alias pi="ssh user_name@rpi"` to `~/.zshrc` or `~/.bashrc`, depending on which shell is being used. Then `pi` does the trick.


## Mac: add passphrase to keychain and configure SSH Hosts
We can avoid typing the SSH key passphrase by adding it to the keychain by using either
```
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```
or
```
ssh-add -K ~/.ssh/id_ed25519
```
depending on the version of MacOS.

Then add the following to `~/.ssh/config` (create this file if it does not exist):
```
Host rpi
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
  User your_pi_user_name
```


## Pi: SSH key pair and add passphrase to keychain
***Note***: This key pair is for enabling the Pi to communicate with, e.g., Github. The set up process is identical to that outlined above for the Mac. Afterwards, in a terminal, do the following:
```
sudo apt-get install keychain
```

Add ``eval `keychain --eval --agents ssh id_ed25519` `` to `~/.bash_profile`. Then everytime we log in (e.g., after rebooting the Pi), the system will ask for the passphrase. We only need to do this once though.


## Some observations
After starting the Pi, gives it a few minutes for it to start to respond to `ping` or `ssh` connection requests. We have also experienced situation where the Pi suddenly stops responding. Just wait a few minutes. It will come back on. 