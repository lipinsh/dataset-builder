# Dataset Builder for Logistics Routes

🚀 **Автоматический сбор данных из Excel-файлов с маршрутами логистики для обучения нейросети**

[![Build Windows Executable](https://github.com/YOUR_USERNAME/dataset-builder/actions/workflows/build-windows.yml/badge.svg)](https://github.com/YOUR_USERNAME/dataset-builder/actions/workflows/build-windows.yml)

## 📥 Скачать готовый .exe файл

### Вариант 1: GitHub Actions (рекомендуется)
1. Перейдите в раздел [Actions](https://github.com/YOUR_USERNAME/dataset-builder/actions)
2. Найдите последний успешный workflow "Build Windows Executable"
3. Скачайте артефакт "DatasetBuilderAdvanced-Windows"

### Вариант 2: GitHub Releases
1. Перейдите в раздел [Releases](https://github.com/YOUR_USERNAME/dataset-builder/releases)
2. Скачайте последнюю версию `DatasetBuilderAdvanced.exe`

## 🔧 Сборка своими руками

### Через GitHub Codespaces (рекомендуется)

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
   
   # Файл будет создан в папке dist/
   ```

### Локально на Windows

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dataset-builder.git
   cd dataset-builder
   ```

2. **Установите Python 3.9+** и зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. **Соберите .exe**:
   ```bash
   python build_advanced_exe.py
   ```

## 🎯 Использование

1. **Запустите** `DatasetBuilderAdvanced.exe`
2. **Введите путь** к папке с Excel файлами (например: `W:\Customers\Natures Way reports\Archive\2024`)
3. **Дождитесь завершения** обработки
4. **Получите результат** в файлах:
   - `combined_dataset.csv`
   - `combined_dataset.parquet`
   - `processing_statistics.csv`
   - `dataset_builder.log`

## 📊 Возможности

- ✅ **Обработка Excel файлов** (.xlsx, .xlsm)
- ✅ **Извлечение дат** из имен файлов
- ✅ **Работа с защищенными листами** (пароль "Test")
- ✅ **Извлечение температуры** из названий клиентов
- ✅ **Обработка листов** "Pallet Order" и "Collection Plan"
- ✅ **Объединение данных** с автоматическим сопоставлением
- ✅ **Накопление данных** (добавление только новых записей)
- ✅ **Сохранение** в CSV и Parquet форматах
- ✅ **Подробное логирование** и статистика

## 📁 Структура входных данных

```
W:\Customers\Natures Way reports\Archive\
├── 2024\
│   ├── January\
│   │   ├── Week 1\
│   │   │   ├── Lyons collections 01012024.xlsx
│   │   │   ├── Lyons collections 02012024.xlsm
│   │   │   └── Lyons collections 03012024 v2.xlsx
│   │   └── Week 2\
│   └── February\
└── 2025\
```

## 🔄 Накопление данных

Программа поддерживает накопление данных:
- При повторном запуске загружается существующий датасет
- Добавляются только новые данные
- Дубликаты не создаются
- Статистика обновляется

## 🛠️ Разработка

### Запуск тестов
```bash
python test_dataset_builder.py
```

### Структура проекта
```
dataset-builder/
├── dataset_builder.py              # Базовая версия
├── dataset_builder_advanced.py     # Улучшенная версия
├── requirements.txt                # Зависимости
├── test_dataset_builder.py         # Тесты
├── build_advanced_exe.py          # Сборка .exe
├── .github/workflows/              # GitHub Actions
└── .devcontainer/                  # Codespaces конфигурация
```

## 📞 Поддержка

- **Issues**: [Создать issue](https://github.com/YOUR_USERNAME/dataset-builder/issues)
- **Discussions**: [Обсуждения](https://github.com/YOUR_USERNAME/dataset-builder/discussions)

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

---

⭐ **Если проект полезен, поставьте звездочку!**
