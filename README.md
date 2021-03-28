# dfva_client
Python integration to DFVA service for digital Signature project

Dependencias necesarias

    sudo apt install swig libpcsclite-dep pcscd

O en fedora

    sudo dnf install swig pcsc-lite-devel pcsc-lite
 
Habilitar el servicio de PCSCD

    sudo systemctl enable pcscd

Crear el archivo para reconocer la tarjeta (si no existe)

    sudo mkdir -p /etc/Athena/
    sudo wget -O /etc/Athena/IDPClientDB.xml https://raw.githubusercontent.com/luisza/dfva_client/master/os_libs/Athena/IDPClientDB.xml
    

# Pasos para generar ejecutable

Instale dependencias 

     sudo dfn install python-virtualenv python-devel
     
Cree un entorno virtual e instale las dependencias

     virtualenv -p python3 venv
     cd dfva_client
     pip install -r requirements.txt
     
  
