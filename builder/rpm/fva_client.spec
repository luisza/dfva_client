Name:           client_fva
Version:        0.2
Release:        1
Summary:        Firma Digital de Costa Rica, aplicación grafica
Source:         %{name}-%{version}.tar.gz
License:        GPLv3+
URL:            https://github.com/luisza/dfva_client/
Requires:       pcsc-lite libxcb  xcb-util

BuildRequires: python3

%description
Cliente de escritorio para firmar y validar documentos de Firma Digital de Costa Rica

%prep
%setup -q -n %{name}


%install 

mkdir -p %{buildroot}/usr/share/client_fva/client_fva/ui/ui_elements/images/
mkdir -p %{buildroot}/usr/share/client_fva/os_libs/linux/x86_64/
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/usr/share/client_fva/certs/
install -m 755  %{_builddir}/%{name}/client_fva.bin %{buildroot}/%{_datadir}/%{name}/client_fva.bin
install -m 755  %{_builddir}/%{name}/client_fva.desktop %{buildroot}/usr/share/applications/client_fva.desktop 
install -m 755  -d %{_builddir}/%{name}/images/ %{buildroot}/%{_datadir}/%{name}/
install -m 755  -C %{_builddir}/%{name}/libASEP11.so %{buildroot}/%{_datadir}/%{name}/libASEP11.so
install -m 755  -C %{_builddir}/%{name}/client_fva_IDPClientDB.xml %{buildroot}/%{_datadir}/%{name}/IDPClientDB.xml
install -m 755  %{_builddir}/%{name}/ca_bundle.pem %{buildroot}/%{_datadir}/%{name}/certs/ca_bundle.pem

%files
%{_datadir}/%{name}/
/usr/share/applications/client_fva.desktop

%post
    mkdir -p /etc/Athena/
    mkdir -p /usr/lib/x86_64-linux-gnu/
    mkdir -p /usr/lib/x64-athena/
    [ \! -e /etc/Athena/IDPClientDB.xml -o -L /etc/Athena/IDPClientDB.xml ] && cp /usr/share/client_fva/IDPClientDB.xml /etc/Athena/IDPClientDB.xml 
    [ \! -e /usr/lib/libASEP11.so -o -L /usr/lib/libASEP11.so ] && cp /usr/share/client_fva/libASEP11.so /usr/lib/libASEP11.so
    [ \! -e /usr/lib/x64-athena/libASEP11.so -o -L /usr/lib/x64-athena/libASEP11.so ] && cp /usr/share/client_fva/libASEP11.so /usr/lib/x64-athena/libASEP11.so
    [ \! -e /usr/lib/x86_64-linux-gnu/libASEP11.so -o -L /usr/lib/x86_64-linux-gnu/libASEP11.so ] && cp /usr/share/client_fva/libASEP11.so /usr/lib/x86_64-linux-gnu/libASEP11.so
    [ \! -e /usr/lib64/libxcb-util.so.1 -o -L /usr/lib64/libxcb-util.so.1 ] && [ -e /usr/lib64/libxcb-util.so.0 -o -L /usr/lib64/libxcb-util.so.0 ]  && ln -s /usr/lib64/libxcb-util.so.0 /usr/lib64/libxcb-util.so.1
%changelog

* Fri Jun 04 2021 Luis Zarate <luisza14@gmail.com> 2.1.5-20
- Primera versión del RPM
