This code was primarily written by Ahmad Mojiri, for the [HILTCRC](https://www.hiltcrc.com.au/) project HILT.RP2.001 "Green hydrogen supply modelling for industry".

## Running stand-alone via Jupyter

Add instructions here.

## Server-based installation

To install the Dash-based GUI for this project on a new server or virtual machine, using the following steps:

1. Install needed system packages:
   ```
   sudo apt install htop byobu apache2 libapache2-mod-wsgi-py3 git man minizinc python3-pip
   ```

2. Install needed python packages (for the root user)
   ```
   sudo pip3 install dash pandas
   ```

3. Install NREL's [System Advisor Model, version 2021-12-01](https://sam.nrel.gov/download/version-2021-12-01.html)
   ```
   wget -Osam.run https://sam.nrel.gov/download/version-2021-12-01/65-sam-2020-11-29-for-linux/file.html
   sudo ./sam.run
   ```
   This will install the files in `/opt/SAM/2020-11-29`
   (there seems to be a problem with the version numbers here!)

4. Install Minizinc from the official packages (Ubuntu's version may be missing some features)

5. Edit the file `apache2/indust.re.conf` to indicate the locations where the repository is located on your machine (we used `/srv/indust.re`)

6. Create a symlink to the above file, then enable the site, via
   ```
   cd /etc/apache/sites-available
   sudo ln -s /path/to/apache2/indust.re.conf
   sudo a2ensite indust.re
   ```

7. Restart apache, `systemctl restart apache2`

8. Open the (ServerAlias as listed in `apache2/indust.re.conf`) site in your browser.
   


