# dfva_client
Python integration to DFVA service for digital Signature project

Dependencias necesarias

sudo apt install swig libpcsclite-dev
sudo apt install pcscd

sudo systemctl enable pcscd

sudo mkdir -p /etc/Athena/

sudo wget -O /etc/Athena/IDPClientDB.xml https://raw.githubusercontent.com/luisza/instaladoresFirmaDigitalCR/master/etc/Athena/IDPClientDB.xml.dist
