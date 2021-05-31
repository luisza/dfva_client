#!/bin/bash

choco install innosetup

OLD_PATH=$(pwd)
echo $OLD_PATH

cd src
sed -i 's/http:\/\/localhost:8000/https:\/\/firmadigital.solvosoft.com/g' client_fva/user_settings.py

pyinstaller --clean --onefile -n client_fva -i client_fva/ui/ui_elements/images/icon.ico --upx-dir=/usr/local/share/  --noconfirm --log-level=WARN --windowed --hidden-import 'pkcs11.defaults' main.py

cd dist
mkdir workdir
EXE_HOMEDIR="workdir"
mkdir -p $EXE_HOMEDIR/System32
mkdir -p $EXE_HOMEDIR/Athena/

cp $OLD_PATH/src/os_libs/windows/asepkcs.dll $EXE_HOMEDIR/System32/
cp $OLD_PATH/src/os_libs/Athena/IDPClientDB.xml $EXE_HOMEDIR/Athena/
cp $OLD_PATH/src/dist/client_fva.exe $EXE_HOMEDIR/

ls -al $EXE_HOMEDIR/
