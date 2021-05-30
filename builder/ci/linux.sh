#!/bin/bash

echo $(whereis python)
OLD_PATH=$(pwd)
cd src

sed -i 's/http:\/\/localhost:8000/https:\/\/firmadigital.solvosoft.com/g' client_fva/user_settings.py
sed -i 's/self.installation_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))/self.installation_path = "\/usr\/share\/client_fva\/"/g'  client_fva/user_settings.py

pyinstaller --clean --onefile -n client_fva -i client_fva/ui/ui_elements/images/icon.ico --upx-dir=/usr/local/share/  --noconfirm --log-level=WARN --windowed --hidden-import 'pkcs11.defaults' main.py

cd dist

DEB_HOMEDIR="${PACKAGE}_${VERSION}_${ARCH}"
mkdir -p $DEB_HOMEDIR/usr/share/client_fva/os_libs/linux/${ARCH}/
mkdir -p $DEB_HOMEDIR/DEBIAN
mkdir -p $DEB_HOMEDIR/etc/Athena/
mkdir -p $DEB_HOMEDIR/usr/lib/x64-athena/
mkdir -p $DEB_HOMEDIR/usr/lib/${ARCH}-linux-gnu/
mkdir -p $DEB_HOMEDIR/usr/share/applications/
mkdir -p $DEB_HOMEDIR/usr/share/client_fva/client_fva/ui/ui_elements/images/

tee -a $DEB_HOMEDIR/DEBIAN/control << END
Package: ${PACKAGE}
Version: ${VERSION}
Architecture: ${ARCH}
Priority: optional
Section: non-free
Depends: pcscd
Homepage: https://github.com/luisza/dfva_client/
Maintainer: Luis Zarate Montero<luisza14@gmail.com>
Description: Cliente para firmar digitalmente documentos
 Este cliente permite firmar documentos electrónicos para Costa Rica usando la firma digital. Además permite validar los documentos.
END

tee -a $DEB_HOMEDIR/usr/share/applications/client_fva.desktop << END
[Desktop Entry]
Name=Cliente FVA
Comment=Firma Digital para Costa Rica
Exec=/usr/share/client_fva/client_fva.bin
Icon=/usr/share/client_fva/client_fva/ui/ui_elements/images/icon.png
Terminal=false
Type=Application
Categories=Network;Application;
StartupNotify=true
END

cp $OLD_PATH/builder/debian/copyright $DEB_HOMEDIR/DEBIAN/
cp $OLD_PATH/builder/debian/postinst $DEB_HOMEDIR/DEBIAN/
sed -i 's/ARCH/'${ARCH}'/g' $DEB_HOMEDIR/DEBIAN/postinst
chmod 0775 $DEB_HOMEDIR/DEBIAN/postinst

cp client_fva $DEB_HOMEDIR/usr/share/client_fva/client_fva.bin
cp $OLD_PATH/src/client_fva/ui/ui_elements/images/* $DEB_HOMEDIR/usr/share/client_fva/client_fva/ui/ui_elements/images/
cp $OLD_PATH/src/os_libs/Athena/IDPClientDB.xml $DEB_HOMEDIR/etc/Athena/client_fva_IDPClientDB.xml
cp $OLD_PATH/src/os_libs/linux/${ARCH}/libASEP11.so $DEB_HOMEDIR/usr/share/client_fva/os_libs/linux/${ARCH}/libASEP11.so
cp -a $OLD_PATH/src/certs/ $DEB_HOMEDIR/usr/share/client_fva/

dpkg-deb --build --root-owner-group $DEB_HOMEDIR
sudo alien -r $DEB_HOMEDIR.deb --scripts
sudo alien -l $DEB_HOMEDIR.deb --scripts
sudo alien -t $DEB_HOMEDIR.deb --scripts

ls -al .
echo $(pwd)

mv ${PACKAGE}_${VERSION}_${ARCH}.deb $OLD_PATH/
mv ${PACKAGE}-${VERSION}-2.${RPM_ARCH}.rpm  $OLD_PATH/
mv lsb-${PACKAGE}-${VERSION}-2.${RPM_ARCH}.rpm $OLD_PATH/
mv ${PACKAGE}-${VERSION}.tgz $OLD_PATH/
 
cd $OLD_PATH
