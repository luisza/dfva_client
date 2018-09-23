#!/bin/bash


pyinstaller --onefile --additional-hooks-dir=hooks main.spec

./dist/main/main
