# 🚀 Быстрый старт - Dataset Builder

## ✅ Что уже готово

Ваш проект полностью настроен и готов к использованию! Все тесты пройдены успешно.

## 📁 Структура проекта

```
build_dataset/
├── dataset_builder.py              # Базовая версия
├── dataset_builder_advanced.py     # Улучшенная версия (рекомендуется)
├── requirements.txt                # Зависимости
├── test_dataset_builder.py         # Тесты
├── build_advanced_exe.py          # Сборка .exe
├── dist/
│   └── DatasetBuilderAdvanced     # Готовый исполняемый файл (macOS)
├── README.md                       # Основная документация
├── INSTALLATION_GUIDE.md          # Подробное руководство
└── PROJECT_SUMMARY.md             # Обзор проекта
```

## 🎯 Как использовать

### Вариант 1: Через Python (рекомендуется для разработки)

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate

# Запустите скрипт
python dataset_builder_advanced.py
```

### Вариант 2: Через исполняемый файл (рекомендуется для пользователей)

```bash
# Перейдите в папку dist
cd dist

# Запустите программу
./DatasetBuilderAdvanced
```

## 📋 Что делать дальше

1. **Запустите программу** одним из способов выше
2. **Введите путь** к папке с Excel файлами (например: `/path/to/your/data/2024`)
3. **Дождитесь завершения** обработки
4. **Получите результат** в файлах:
   - `combined_dataset.csv`
   - `combined_dataset.parquet`
   - `processing_statistics.csv`
   - `dataset_builder.log`

## 🔧 Если нужно собрать .exe для Windows

```bash
# Активируйте виртуальное окружение
source .venv/bin/activate

# Запустите сборку
python build_advanced_exe.py
```

## ✅ Проверка работоспособности

Запустите тесты для проверки:

```bash
source .venv/bin/activate
python test_dataset_builder.py
```

## 🎉 Готово!

Ваш Dataset Builder полностью готов к работе! Все функции протестированы и работают корректно.
