# Fingers in the Pi

This website documents how we (a 40+ man and a 10- boy) set up and experiment with our Raspberry 4 Model B with 4Gb RAM. We would be thrilled if you find any of the stuff useful. 

# Setting up the Pi (with SSH and VS Code)
The following are the steps we used to set up .  

- Format the micro SD to `MS-DOS (FAT32)`.

- Download NOOBS, the full version, not the lite version, from `https://downloads.raspberrypi.org`. Uncompress the downloaded file and save the contents to the micro SD card using `unzip NOOBS_v3_8_1.zip -d path_to_sd_card`.  

- Put the Pi into the official case by first sliding the Pi under the little pertruding bit between the two mini-HDMI ports, then pushing the Pi down far enough, so that the two studs at the bottom of the case (on the opposite side of the USB-C socket) slotted into the holes in the Pi. 
 
- Insert the micro SD, connect the Pi to screen/mouse/keyboard, then plug it in. The lights on the Pi started to flash and the screen lit up shortly afterwards. We set up the WIFI, and then installed *Raspberry Pi OS Full (32-bit) with desktop and recommended software*. The installation took less than 10 minutes. Then the Pi rebooted into the new OS automatically. We followed the on-screen instructions to choose a location and set up an account. Updating the OS took a while, but the process went smoothly, requiring no user input.

- In "Preferences (access via top-right raspberry icon) > Paspberry Pi Configuration":
  - For extra security, turn off "System > Auto Login".
  - In "Interfaces", enable "SSH" (for accessing remote from another computer within our home network).
  - Click "OK" to confirm changes.

- Find out the IP address by issuing `ip addr` in the terminal. On another compute on the same network, issue `ssh $ip_addr`, where `$ip_addr` is the value returned by the previous step.

- To avoid having to type password to log in via SSH everytime, create an SSH key pair on the other computer (not the Pi):
  - `ssh-keygen -t ed25519 -C "email@server.com"`, enter a passphrase and save file to the default location.
  - Add the SSH key to `ssh-agent` by using 
    ```
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    ```
  - Add the public key to the Pi by `ssh-copy-id user_name@ip_addr`, where user_name should be replaced by the actual user name of the Pi, and ip_addr is the IP address of the Pi. We should now be able to use `ssh user_name@ip_addr` without entering the Pi's password.
  - If the home broadband router permits, set it up so that it gives the Pi the same IP address everytime. Then on the non-Pi machine add `ip_addr rpi` to `/etc/hosts`, where `rpi` can be any other easy-to-remember name (this step requires `sudo` privilege). We can log in just using `ssh user_name@rpi`.
  - To make things even easier, on the non-Pi machine, add `alias pi="ssh user_name@rpi"` to `~/.zshrc` or `~/.bashrc`, depending on which shell is being used. Then `pi` does the trick.


- Install VS Code on the non-Pi machine
  - Add the Remote Development extension pack.
  - Open the control pallete and type `Remote-SSH: Connect to Host` > `Configure SSH Hosts`, then select the `config` file in the `.ssh` folder in your home directory. Add something similar to the following to the file:
  ```
  Host rpi
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519
    User your_pi_user_name
  ```
  
  Once the above changes have been saved, you can click on the `Remote Development` icon in the left-hand bar of the window. `rpi` should appear. Click on the open folder icon to the right of `rpi` to open a folder on the Pi. VS Code will remember this folder has been opened before. So next time when we click on the Remote Development icon, we will see a list of folders that we have worked on before.

  


# Creating a `venv` for python development
The version of Raspberry Pi OS cames with `python 3.9.2`, which was sufficient for our purpose. However, it is good practice to use a local environment for each project, so that different projects do not clash with one another. The following creates a new environment in a local folder named `venv`.
```
python -m venv --copies --clear ./venv
source ./venv/bin/activate
```

The name `venv` should appear in thecommand prompt, indicating that the environment has been activate. New packages can now be installed using `pip`.

Use `deactivate` to exit the environment.


# Set up a python project in VS Code with git and readthedocs
- Use equivalent steps to create a SSH key pair for the Pi. On you Github account, in "Settings > SSH and GPG keys", add the Pi's public key. 

- Create a repo on Github. On the repo's homepage, find a large green button named "Code", and copy the contents of SSH into the clip board.

- Open a terminal on the Pi, go to a desired location, and issue `git clone contents_in_clipboard`. If `git` has not been installed on, do `sudo apt-get install git` first.

- We will primarily be doing remote development using VS Code. Use the previous step to connect to the Pi remotely in VS Code. Open the folder created by `git clone`. 
  
- First we need to install the Python extension pack in VS Code. The `Black Formatter` extension could also be installed to help automatical code formatting. Then open the control pallete, type `Python: Select Interpreter` > "+ Enter interpreter path...". In the window, find the folder that contains the `venv`, and within it, locate `bin/python`.

- To use Markdown to write documentation, we use `mkdocs`. Go to the project's folder, and activate the `venv` using the steps described above. Issue `pip install mkdocs` to add the tool into the `venv`. Then while at the top level of the project's folder, use `mkdocs new .` to create a new Markdown documentation set-up. This will add a folder `docs` and `mkdocs.yml` to the project. In `docs`, we will find `index.md`. This is the total level entry point for our documentation.

- Go to `https://readthedocs.org/` and follow the tutorial on setting up an account and importing projects from Github. 
  On "Project Details" page, check "Edit advanced project options" before clicking on "Next". On the next page, change "Documentation type" to "Mkdocs". 
  
- After the project has been imported, click on the "Admin" button. The go to "Adavanced settings", and check "Build pull requests for this project".



