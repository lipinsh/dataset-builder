#!/bin/bash

# Скрипт для настройки Git репозитория и загрузки на GitHub

echo "🚀 Настройка Git репозитория для Dataset Builder"

# Проверяем, что Git установлен
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и попробуйте снова."
    exit 1
fi

# Инициализируем Git репозиторий
echo "📁 Инициализация Git репозитория..."
git init

# Добавляем все файлы
echo "📝 Добавление файлов в Git..."
git add .

# Создаем первый коммит
echo "💾 Создание первого коммита..."
git commit -m "Initial commit: Dataset Builder for Logistics Routes

- ✅ Обработка Excel файлов (.xlsx, .xlsm)
- ✅ Извлечение данных из листов 'Pallet Order' и 'Collection Plan'
- ✅ Объединение заказов и доставок
- ✅ Сохранение в CSV и Parquet форматах
- ✅ Поддержка накопления данных
- ✅ Подробное логирование и статистика
- ✅ GitHub Actions для автоматической сборки .exe
- ✅ GitHub Codespaces конфигурация"

echo ""
echo "🎉 Git репозиторий настроен!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте новый репозиторий на GitHub:"
echo "   - Перейдите на https://github.com/new"
echo "   - Назовите репозиторий 'dataset-builder'"
echo "   - НЕ инициализируйте с README (у нас уже есть)"
echo ""
echo "2. Добавьте удаленный репозиторий:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/dataset-builder.git"
echo ""
echo "3. Загрузите код на GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. После загрузки на GitHub:"
echo "   - GitHub Actions автоматически соберет .exe файл для Windows"
echo "   - Вы сможете скачать его из раздела Actions или Releases"
echo "   - Или использовать GitHub Codespaces для сборки"
echo ""
echo "🔗 Замените 'YOUR_USERNAME' на ваше имя пользователя GitHub"
