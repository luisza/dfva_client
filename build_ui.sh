#!/bin/bash


pyuic5 client_fva/ui/ui_elements/requestsignature.ui -o client_fva/ui/requestsignatureui.py -x
sed -i 's/import resources_rc/from . import resources_rc/g' client_fva/ui/requestsignatureui.py
