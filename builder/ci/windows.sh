#!/bin/bash

choco install innosetup sqlite
cat /c/ProgramData/chocolatey/logs/chocolatey.log

OLD_PATH=$(pwd)
echo $OLD_PATH

cd src
sed -i 's/http:\/\/localhost:8000/https:\/\/firmadigital.solvosoft.com/g' client_fva/user_settings.py

pyinstaller --clean --onefile -n client_fva -i client_fva/ui/ui_elements/images/icon.ico --upx-dir=/usr/local/share/  --noconfirm --log-level=WARN --windowed --noconsole --hidden-import 'pkcs11.defaults' main.py

cd dist
mkdir workdir
EXE_HOMEDIR="workdir"
mkdir -p $EXE_HOMEDIR/


cp $OLD_PATH/src/os_libs/windows/asepkcs.dll $EXE_HOMEDIR/
cp $OLD_PATH/src/dist/client_fva.exe $EXE_HOMEDIR/
cp $OLD_PATH/src/client_fva/ui/ui_elements/images/icon.png $EXE_HOMEDIR/
cp $OLD_PATH/src/client_fva/ui/ui_elements/images/icon.ico $EXE_HOMEDIR/
cp $OLD_PATH/src/os_libs/windows/installer.iss $EXE_HOMEDIR/

cd $EXE_HOMEDIR/
iscc installer.iss

ls -al Output
