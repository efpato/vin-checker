vin-checker
================

VIN Checker

#Настройка локальной машины для запуска скрипта
 
 1. Установить Google Chrome
 2. Скачать [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (версия как у браузера) и положить в C:\Windows
 3. Установить [Python](https://www.python.org/downloads/windows/)
 4. Прописать в переменную окружения PATH к установленному каталогу с python.exe (по умолчанию это C:\Python3\) и добавить путь к C:\Python3\Scripts
 5. Установить [git-клиента](https://git-scm.com/downloads)
 6. Запустить консоль git
 7. Клонировать репозиторий себе на локальную машину
```bash
git clone https://github.com/efpato/vin-checker.git
```
 8. Перейти в склонированный каталог и выполнить:
```bash
cd vin-checker
pip install -r requirements.txt
```

УСПЕХ! Вы готовы к использованию скрипта локально на своей виндовой машине

#Использование

```bash
python vinchk VIN1 VIN2 ... VINN
```
