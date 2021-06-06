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
sed -ie 's/self.installation_path = None/self.installation_path = "\/usr\/local\/client_fva\/"/g'  client_fva/user_settings.py

pyinstaller --clean --onefile -n client_fva -i client_fva/ui/ui_elements/images/icon.icns --upx-dir=/usr/local/share/  --noconfirm --log-level=WARN --windowed  --hidden-import 'pkcs11.defaults' main.py


mkdir -p dist/package/usr/local/client_fva/os_libs/macos/
mkdir -p dist/package/usr/local/client_fva/certs
mkdir -p dist/package/usr/local/client_fva/etc/Athena/
mkdir -p dist/scripts


#mv dist/client_fva.app dist/Cliente\ FVA.app
cp -a dist/client_fva.app dist/package/usr/local/client_fva/
cp -a certs/ca_bundle.pem dist/package/usr/local/client_fva/certs/
cp -a os_libs/macos/libASEP11.dylib dist/package/usr/local/client_fva/os_libs/macos/
cp -a os_libs/Athena/IDPClientDB.xml  dist/package/usr/local/client_fva/etc/Athena/
tar -C dist/ -cf dist/package/usr/local/client_fva/client_fva.app.tar client_fva.app

tee -a dist/scripts/postinstall << END
#!/bin/sh
tar -C /Applications -xf /usr/local/client_fva/client_fva.app.tar
mv /Applications/client_fva.app  /Applications/Cliente\ FVA.app
mkdir -p /etc/Athena/
cp /usr/local/client_fva/etc/Athena/IDPClientDB.xml /etc/Athena/

[ \! -e /usr/local/lib/libASEP11.dylib -o -L /usr/local/lib/libASEP11.dylib ] && cp /usr/local/client_fva/os_libs/macos/libASEP11.dylib /usr/local/lib/libASEP11.dylib

exit 0 # all good
END
chmod u+x dist/scripts/postinstall

cd dist


pkgbuild --root ./package --identifier cr.clientfva  --script ./scripts --version 0.2 --install-location / ./dfva_client.pkg

