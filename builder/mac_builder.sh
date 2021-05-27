#!/bin/zsh

source /etc/profile
export LC_ALL="en_US.UTF-8"
if [ -d "src" ]; then
 rm -r src
fi
DIR=venv
tar -zxf dfvaclient.tar.gz 
if [ -d "$DIR" ]; then
    source venv/bin/activate
else
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install  pyinstaller
fi

cd src/
sed -ie 's/http:\/\/localhost:8000/https:\/\/firmadigital.solvosoft.com/g' client_fva/user_settings.py

pyinstaller --clean --onefile -n client_fva -i client_fva/ui/ui_elements/images/icon.ico --upx-dir=/usr/local/share/  --noconfirm --log-level=WARN --windowed  --hidden-import 'pkcs11.defaults'  --add-data certs:Contents/Resources/certs --add-data os_libs/macos/libASEP11.dylib:Contents/Resources/os_libs/macos/libASEP11.dylib  --add-data os_libs/Athena/IDPClientDB.xml:/etc/Athena/IDPClientDB.xml  main.py

#rm -r requirements.txt src
