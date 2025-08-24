# 🚀 Загрузка проекта на GitHub

## 📋 Пошаговая инструкция

### 1. Подготовка проекта

У вас уже есть готовый проект с настроенным Git репозиторием. Запустите скрипт настройки:

```bash
./setup_github.sh
```

### 2. Создание репозитория на GitHub

1. **Перейдите на GitHub**: https://github.com/new
2. **Название репозитория**: `dataset-builder`
3. **Описание**: `Dataset Builder for Logistics Routes - автоматический сбор данных из Excel файлов`
4. **Приватность**: Выберите Public или Private
5. **ВАЖНО**: НЕ ставьте галочки "Add a README file", "Add .gitignore", "Choose a license" - у нас уже есть эти файлы
6. **Нажмите**: "Create repository"

### 3. Загрузка кода на GitHub

После создания репозитория выполните команды (замените `YOUR_USERNAME` на ваше имя пользователя):

```bash
# Добавляем удаленный репозиторий
git remote add origin https://github.com/YOUR_USERNAME/dataset-builder.git

# Переименовываем ветку в main
git branch -M main

# Загружаем код на GitHub
git push -u origin main
```

### 4. Проверка загрузки

1. Перейдите на страницу вашего репозитория: `https://github.com/YOUR_USERNAME/dataset-builder`
2. Убедитесь, что все файлы загружены
3. Проверьте, что GitHub Actions запустились автоматически

## 🔧 Получение .exe файла для Windows

### Вариант 1: GitHub Actions (автоматически)

1. **Перейдите в раздел Actions**: https://github.com/YOUR_USERNAME/dataset-builder/actions
2. **Найдите workflow "Build Windows Executable"**
3. **Дождитесь завершения** (зеленая галочка)
4. **Скачайте артефакт**:
   - Нажмите на workflow
   - Прокрутите вниз до "Artifacts"
   - Скачайте "DatasetBuilderAdvanced-Windows"

### Вариант 2: GitHub Codespaces

1. **Откройте Codespaces**:
   - Нажмите кнопку "Code" в репозитории
   - Выберите вкладку "Codespaces"
   - Нажмите "Create codespace on main"

2. **В Codespaces выполните**:
   ```bash
   # Установите зависимости
   pip install -r requirements.txt
   
   # Соберите .exe файл
   python build_advanced_exe.py
   
   # Скачайте файл из папки dist/
   ```

### Вариант 3: GitHub Releases

После успешного выполнения GitHub Actions:
1. Перейдите в раздел [Releases](https://github.com/YOUR_USERNAME/dataset-builder/releases)
2. Скачайте `DatasetBuilderAdvanced.exe`

## 📁 Структура репозитория

```
dataset-builder/
├── 📄 dataset_builder.py              # Базовая версия
├── 📄 dataset_builder_advanced.py     # Улучшенная версия
├── 📄 requirements.txt                # Зависимости
├── 📄 test_dataset_builder.py         # Тесты
├── 📄 build_advanced_exe.py          # Сборка .exe
├── 📄 README_GITHUB.md               # README для GitHub
├── 📄 LICENSE                        # Лицензия MIT
├── 📄 .gitignore                     # Исключения Git
├── 📁 .github/workflows/             # GitHub Actions
│   └── 📄 build-windows.yml         # Автоматическая сборка
└── 📁 .devcontainer/                 # Codespaces конфигурация
    └── 📄 devcontainer.json         # Настройки контейнера
```

## 🎯 Что происходит после загрузки

### GitHub Actions автоматически:
- ✅ Установит Python 3.9 на Windows
- ✅ Установит все зависимости
- ✅ Соберет .exe файл
- ✅ Загрузит артефакт для скачивания
- ✅ Создаст Release с .exe файлом

### Вы получите:
- 📥 Готовый .exe файл для Windows
- 📋 Подробную документацию
- 🔧 Возможность использовать Codespaces
- 📊 Автоматические тесты

## 🆘 Устранение проблем

### Ошибка "Permission denied"
```bash
# Проверьте права доступа
ls -la setup_github.sh
# Если нужно, сделайте исполняемым
chmod +x setup_github.sh
```

### Ошибка "Repository not found"
- Проверьте правильность URL репозитория
- Убедитесь, что репозиторий создан на GitHub
- Проверьте права доступа к репозиторию

### GitHub Actions не запустились
- Проверьте, что файл `.github/workflows/build-windows.yml` загружен
- Убедитесь, что репозиторий публичный или у вас есть права на Actions

## 🎉 Готово!

После выполнения всех шагов у вас будет:
- ✅ Код на GitHub
- ✅ Автоматическая сборка .exe файлов
- ✅ Готовый .exe файл для Windows
- ✅ Возможность использовать Codespaces

**Теперь вы можете скачать .exe файл и использовать его на Windows компьютере!** 🚀
