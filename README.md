# TheSubmarine

## Назначение

В игре **TheSubmarine** вы выступаете в роли капитана подводной лодки. Вам необходимо спасти всех водолазов, которые застряли на глубине и избежать столкновения с рыбами.
В вашем распоряжении ограниченное количество воздуха и жизненной энергии. Воздух тратится под водой и его можно пополнить только всплыв на поверхность моря.

Игра относится к "бесконечным играм" в которых игрок рано или поздно проиграет.


## Управление

Для управления используются клавиши:

- стрелка вверх (UO)
- стрелка вниз (DOWN)
- стрелка влево (LEFT)
- стрелка вправо (RIGHT)
- клавиша ввода (ENTER)
- пробел (SPACE)
- клавиша ESCAPE

Выбор пунктов меню осуществляется с помощью клавиш управления курсором, а подтверждение действий в выбранном пункте меню можно выполнить с помощью клавишу ввода (ENTER)


## Системные требования

Работа приложения проверялась в **Python 3.9.1** под управлением операционной системы Windows 10 и Xubuntu 20.04.

Для корректной работы приложения необходимо установить следующие библиотеки:

- pygame
  ```cmd
  pip install pygame
  ```

Смотри файл [requirements.txt](requirements.txt).

## Порядок сборки проекта в автономное приложение

**Запуск приложения:**

Для запуска приложения неоходимо установить все недостающие компоненты. После этого запустить файл **main.py**

**Известные проблемы:**

- Убедитесь, что установлен python последней версии
- При необходимости установите недостающие модули

**Сборка приложения**

Для сборки автономного приложения требуется установить модуль **pyinstaller** и выполнить команду:  

```cmd
pyinstaller --onefile --noconsole main.py
```
 
После этого необходимо получившийся файл **main.exe** из каталога **dist** поместить в каталог проекта (в ту  папку, где находится каталог **data**)


## Что еще можно доделать

Много чего хотелось бы добавить, например:

- возможность автоматического скролинга мира при движении вправо
- больше анимации и разнообразных спрайтов

## Ресурсы

### Музыка:

- [underwater_mind (2011) the guta jasna](https://www.jamendo.com/track/854045/underwater_mind)
- [Deep Underwater Panda](https://www.jamendo.com/album/187523/deep-underwater)

### Звуки:
- [menu1.wav](https://zvukogram.com/index.php?r=site/download&id=4605&type=wav)
- [много разных звуковых эффектов](https://zvukogram.com/category/zvuki-vyibora-knopki-v-menyu/)

### Изображения:

- [player1.png](откуда то из сети)
- [bird.png](откуда то из сети)
- [diver.png](https://cdn4.vectorstock.com/i/1000x1000/94/83/diver-boy-swimming-sprite-vector-3509483.jpg)

## P.S.

Персональный проект в рамках подготовки преподавателей второго года обучения ЯЛ.
