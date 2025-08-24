# Инструкции для Windows

## 🎯 Что делать на Windows:

1. **Скачайте и распакуйте** архив `DatasetBuilder_Windows_*.zip`

2. **Установите Python** (если не установлен):
   - Перейдите на https://www.python.org/downloads/
   - Скачайте Python 3.8 или выше
   - При установке **ОБЯЗАТЕЛЬНО** отметьте "Add Python to PATH"

3. **Установите зависимости**:
   - Откройте командную строку в папке с файлами
   - Выполните: `pip install -r requirements.txt`

4. **Запустите программу**:
   - Выполните: `python dataset_builder_advanced.py`
   - Или дважды кликните на `run.bat`

## 🔧 Создание .exe файла:

```cmd
pip install pyinstaller
pyinstaller --onefile --console --name=DatasetBuilderAdvanced dataset_builder_advanced.py
```

## 📁 Структура файлов:

- `dataset_builder_advanced.py` - основной скрипт
- `requirements.txt` - зависимости
- `install.bat` - автоматическая установка
- `run.bat` - запуск программы
- `README.md` - документация
- `WINDOWS_README.md` - инструкции для Windows

## ⚠️ Важно:

- Убедитесь, что Python добавлен в PATH
- Запускайте командную строку от имени администратора при необходимости
- Проверьте, что антивирус не блокирует Python
