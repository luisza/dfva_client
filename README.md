# dfva_client
Python integration to DFVA service for digital Signature project

Dependencias necesarias

    sudo apt install swig libpcsclite-dev pcscd

O en fedora

    sudo dnf install swig pcsc-lite-devel pcsc-lite
 
Habilitar el servicio de PCSCD

    sudo systemctl enable pcscd

Crear el archivo para reconocer la tarjeta (si no existe)

    sudo mkdir -p /etc/Athena/
    sudo wget -O /etc/Athena/IDPClientDB.xml https://raw.githubusercontent.com/luisza/dfva_client/master/os_libs/Athena/IDPClientDB.xml
    

# Pasos para generar ejecutable

Instale dependencias 

     sudo apt install virtualenv python3-dev libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxkbcommon-x11-0 libxcb-xkb1 libxcb-render-util0 libxcb-keysyms1 libxcb-util0 libxcb-randr0
     sudo dfn install python-virtualenv python-devel
     
Cree un entorno virtual e instale las dependencias

     virtualenv -p python3 venv
     cd dfva_client
     pip install -r requirements.txt
     
  
# solo para debian estable

Debian estable tiene una dependencia no cumplida con la última versión de QT5, por lo que hay que instalar la dependencia manual

    wget http://ftp.us.debian.org/debian/pool/main/x/xcb-util/libxcb-util1_0.4.0-1+b1_amd64.deb
    sudo dpkg -i libxcb-util1_0.4.0-1+b1_amd64.deb
 
