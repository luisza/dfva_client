#!/bin/bash

sed -i 's/http:\/\/localhost:8000/https:\/\/firmadigital.solvosoft.com/g' source/client_fva/user_settings.py
sed -i 's/self.installation_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))/self.installation_path = "\/usr\/share\/client_fva\/"/g'  source/client_fva/user_settings.py

cd source/

pyinstaller --clean --onefile -n client_fva -i client_fva/ui/ui_elements/images/icon.png --upx-dir=/usr/local/share/  --noconfirm --log-level=WARN --windowed --hidden-import 'pkcs11.defaults' main.py



DEB_HOMEDIR=~/rpmbuild/$NAME
mkdir -p $DEB_HOMEDIR
mkdir -p  ~/rpmbuild/$NAME/


cp dist/client_fva $DEB_HOMEDIR/client_fva.bin
cp -ar ~/source/client_fva/ui/ui_elements/images $DEB_HOMEDIR/
cp ~/source/os_libs/Athena/IDPClientDB.xml $DEB_HOMEDIR/client_fva_IDPClientDB.xml
cp ~/source/os_libs/linux/${ARCH}/libASEP11.so $DEB_HOMEDIR/libASEP11.so
cp -a ~/source/certs/* $DEB_HOMEDIR/

tee -a $DEB_HOMEDIR/client_fva.desktop << END
[Desktop Entry]
Name=Cliente FVA
Comment=Firma Digital para Costa Rica
Exec=/usr/share/client_fva/client_fva.bin
Icon=/usr/share/client_fva/icon.png
Terminal=false
Type=Application
Categories=Network;Application;
StartupNotify=true
END

cd ~/rpmbuild/
tar -zcf ~/rpmbuild/SOURCES/${NAME}-${VERSION}.tar.gz $NAME

sed -i 's/Name:           client_fva/Name:           '${NAME}'/g' SPECS/fva_client.spec
sed -i 's/Version:        0.2/Version:           '${VERSION}'/g' SPECS/fva_client.spec
rpmbuild -ba SPECS/fva_client.spec || exit 1

mv  ~/rpmbuild/RPMS/x86_64/${NAME}-${VERSION}-1.x86_64.rpm /packages/${NAME}-${VERSION}-1.${OS}.x86_64.rpm


