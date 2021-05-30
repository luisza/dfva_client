#  brew install graphicsmagick imagemagick
#

tar zcf dfvaclient.tar.gz src requirements.txt
scp  dfvaclient.tar.gz luisza@192.168.122.186:~/Desktop/
scp  builder/mac_builder.sh luisza@192.168.122.186:~/Desktop/mac_builder.sh
ssh luisza@192.168.122.186 -t 'cd ~/Desktop && zsh mac_builder.sh'
