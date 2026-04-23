# Как загрузить проект на GitHub

## Если репозиторий на GitHub пустой

1. Открой PowerShell.
2. Выполни команды:

```powershell
cd "C:\Users\neeth\OneDrive\Desktop\практика алина\electrotool-accounting-app"
git init
git branch -M main
git add .
git commit -m "Добавлен проект учета электроинструмента"
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Вместо `https://github.com/USERNAME/REPOSITORY.git` вставь ссылку на её репозиторий.

## Если в репозитории уже есть файлы

Лучше сначала скачать репозиторий, потом перенести туда файлы проекта:

```powershell
cd "C:\Users\neeth\OneDrive\Desktop"
git clone https://github.com/USERNAME/REPOSITORY.git
Copy-Item -Path "C:\Users\neeth\OneDrive\Desktop\практика алина\electrotool-accounting-app\*" -Destination ".\REPOSITORY" -Recurse -Force
cd ".\REPOSITORY"
git add .
git commit -m "Добавлен проект учета электроинструмента"
git push
```

## Если GitHub попросит вход

Откроется окно входа GitHub. Выбери вход через браузер или Google, подтверди доступ и снова выполни `git push`, если команда не продолжилась автоматически.
