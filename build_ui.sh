#!/bin/bash


function build_ui_py(){
  pyuic5 client_fva/ui/ui_elements/$1.ui -o client_fva/ui/$1ui.py -x
  if [ "$(uname)" == "Darwin" ]; then
    sed -i '' 's/import resources_rc/from . import resources_rc/g' client_fva/ui/$1ui.py
  else
    sed -i 's/import resources_rc/from . import resources_rc/g' client_fva/ui/$1ui.py
  fi
}

function build_all() {
  build_ui_py contactAddDialog
  build_ui_py fvadialog
  build_ui_py managecontacts
  build_ui_py mysignatures
  build_ui_py requestsignature
  build_ui_py signvalidate
  build_ui_py fvaclient
  build_ui_py managecontactgroups
  build_ui_py myrequests
  build_ui_py requestauthentication
  build_ui_py settings
  build_ui_py tabdefault
  build_ui_py validationinformation
  build_ui_py validationinformationcertificate
}

if [ "$#" -eq  "0" ]
 then
   echo "Creando todos, si solo quiere uno ejecute build_ui.sh fvaclientui"
   build_all
else
   build_ui_py $1
fi
