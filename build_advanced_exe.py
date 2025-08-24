#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Build script for creating executable file
Скрипт для сборки .exe файла улучшенной версии
"""

import os
import subprocess
import sys
import shutil

def install_requirements():
    """Устанавливает необходимые зависимости"""
    print("Устанавливаю зависимости...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Зависимости установлены")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller установлен")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки PyInstaller: {e}")
        return False
    
    return True

def clean_build_dirs():
    """Очищает папки сборки"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Очищена папка: {dir_name}")
            except Exception as e:
                print(f"⚠️ Не удалось очистить папку {dir_name}: {e}")

def build_exe():
    """Собирает .exe файл"""
    print("Собираю .exe файл...")
    
    # Определяем правильный разделитель для --add-data в зависимости от ОС
    import platform
    if platform.system() == "Windows":
        data_separator = ";"
    else:
        data_separator = ":"
    
    # Команда для PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Один файл
        "--console",  # Консольное приложение
        "--name=DatasetBuilderAdvanced",  # Имя выходного файла
        f"--add-data=requirements.txt{data_separator}.",  # Включаем requirements.txt
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=pyarrow",
        "--hidden-import=fastparquet",
        "--hidden-import=xlrd",
        "--hidden-import=logging",
        "--hidden-import=typing",
        "--hidden-import=pathlib",
        "--hidden-import=glob",
        "--hidden-import=re",
        "--hidden-import=datetime",
        "--hidden-import=warnings",
        "--clean",  # Очистка кэша
        "dataset_builder_advanced.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✓ Сборка завершена успешно!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки: {e}")
        return False

def verify_exe():
    """Проверяет созданный исполняемый файл"""
    import platform
    
    # Определяем правильное имя файла в зависимости от ОС
    if platform.system() == "Windows":
        exe_name = "DatasetBuilderAdvanced.exe"
    else:
        exe_name = "DatasetBuilderAdvanced"
    
    exe_path = f"dist/{exe_name}"
    
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"✓ Исполняемый файл создан: {exe_path}")
        print(f"✓ Размер файла: {file_size:.1f} MB")
        return True
    else:
        print(f"❌ Исполняемый файл не найден: {exe_path}")
        return False

def create_launcher_script():
    """Создает bat-файл для запуска"""
    bat_content = """@echo off
echo === Dataset Builder for Logistics Routes ===
echo.
echo Запуск программы...
echo.
DatasetBuilderAdvanced.exe
echo.
echo Нажмите любую клавишу для выхода...
pause > nul
"""
    
    bat_path = "dist/run_dataset_builder.bat"
    try:
        with open(bat_path, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        print(f"✓ Создан bat-файл: {bat_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания bat-файла: {e}")
        return False

def copy_documentation():
    """Копирует документацию в папку dist"""
    files_to_copy = ['README.md']
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            try:
                shutil.copy2(file_name, f"dist/{file_name}")
                print(f"✓ Скопирован файл: {file_name}")
            except Exception as e:
                print(f"⚠️ Не удалось скопировать {file_name}: {e}")

def main():
    """Основная функция"""
    print("=== Advanced Dataset Builder - Build Script ===")
    print("Сборка исполняемого файла")
    print()
    
    try:
        # Очищаем папки сборки
        clean_build_dirs()
        
        # Устанавливаем зависимости
        if not install_requirements():
            print("❌ Не удалось установить зависимости")
            input("Нажмите Enter для выхода...")
            return
        
        # Собираем .exe
        if not build_exe():
            print("❌ Не удалось собрать .exe файл")
            input("Нажмите Enter для выхода...")
            return
        
        # Проверяем результат
        if not verify_exe():
            print("❌ Исполняемый файл не создан")
            input("Нажмите Enter для выхода...")
            return
        
        # Создаем bat-файл
        create_launcher_script()
        
        # Копируем документацию
        copy_documentation()
        
        print("\n🎉 Сборка завершена успешно!")
        print("\nФайлы в папке dist/:")
        print("- DatasetBuilderAdvanced.exe (основной исполняемый файл)")
        print("- run_dataset_builder.bat (файл для запуска)")
        print("- README.md (документация)")
        print("\nДля использования:")
        print("1. Скопируйте папку dist/ на целевой компьютер")
        print("2. Запустите run_dataset_builder.bat или DatasetBuilderAdvanced.exe")
        
    except Exception as e:
        print(f"❌ Критическая ошибка сборки: {e}")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
