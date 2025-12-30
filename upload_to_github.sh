#!/bin/bash

# 🚀 Скрипт для швидкого завантаження на GitHub
# Використання: ./upload_to_github.sh

echo "🔐 SM4 Encryption Utility - Upload to GitHub"
echo "=============================================="
echo ""

# Перевірка чи git встановлено
if ! command -v git &> /dev/null; then
    echo "❌ Git не встановлено!"
    echo "Встановіть: sudo apt install git"
    exit 1
fi

# Запит username
read -p "Введіть ваш GitHub username: " username

if [ -z "$username" ]; then
    echo "❌ Username не може бути порожнім!"
    exit 1
fi

# Назва репозиторію
repo_name="SM4-Encryption-Utility"

echo ""
echo "📝 Використовуватиметься:"
echo "   Repository: https://github.com/$username/$repo_name"
echo ""
read -p "Продовжити? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Скасовано"
    exit 0
fi

echo ""
echo "🔧 Ініціалізація Git..."

# Перевірка чи вже є git репозиторій
if [ -d ".git" ]; then
    echo "⚠️  Git вже ініціалізовано"
else
    git init
    echo "✅ Git ініціалізовано"
fi

echo ""
echo "📦 Додавання файлів..."
git add .

echo ""
echo "💾 Створення коміту..."
git commit -m "🎉 Initial commit: SM4 Encryption Utility with bilingual UI (UA/EN)"

echo ""
echo "🔗 Підключення до GitHub..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$username/$repo_name.git"

echo ""
echo "🌿 Перемикання на гілку main..."
git branch -M main

echo ""
echo "📤 Завантаження на GitHub..."
echo ""
echo "⚠️  ВАЖЛИВО: Використовуйте Personal Access Token як пароль!"
echo "   (не звичайний пароль від GitHub)"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Успіх! Проект завантажено на GitHub!"
    echo ""
    echo "🌐 Відкрийте у браузері:"
    echo "   https://github.com/$username/$repo_name"
    echo ""
else
    echo ""
    echo "❌ Помилка при завантаженні!"
    echo ""
    echo "💡 Можливі причини:"
    echo "   1. Репозиторій ще не створено на GitHub"
    echo "   2. Неправильний username"
    echo "   3. Немає доступу до репозиторію"
    echo "   4. Потрібен Personal Access Token"
    echo ""
    echo "📚 Дивіться: GITHUB_GUIDE.md для детальних інструкцій"
fi
