#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating executable file
Скрипт для сборки .exe файла с помощью PyInstaller
"""

import os
import subprocess
import sys

def install_requirements():
    """Устанавливает необходимые зависимости"""
    print("Устанавливаю зависимости...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    """Собирает .exe файл"""
    print("Собираю .exe файл...")
    
    # Команда для PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Один файл
        "--console",  # Консольное приложение
        "--name=DatasetBuilder",  # Имя выходного файла
        "--add-data=requirements.txt;.",  # Включаем requirements.txt
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=pyarrow",
        "--hidden-import=fastparquet",
        "--hidden-import=xlrd",
        "dataset_builder.py"
    ]
    
    subprocess.check_call(cmd)
    
    print("Сборка завершена!")
    print("Исполняемый файл находится в папке dist/DatasetBuilder.exe")

def main():
    """Основная функция"""
    try:
        print("=== Dataset Builder - Build Script ===")
        
        # Устанавливаем зависимости
        install_requirements()
        
        # Собираем .exe
        build_exe()
        
        print("\nГотово! Можете использовать DatasetBuilder.exe")
        
    except Exception as e:
        print(f"Ошибка сборки: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
