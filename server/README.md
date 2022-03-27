Для запуска сервера нужно будет установить c++ компилятор (https://www.microsoft.com/ru-ru/download/details.aspx?id=48159).

Также необходимо установить MongoDB Community Server 5.0.6+ (пакет msi) https://www.mongodb.com/try/download/community

Запуск сервера MongoDB (по умолчанию в C:\Program Files\MongoDB\Server\*.*\bin) через cmd: 
`mongod`

Далее нужно скачать conda (https://www.anaconda.com/products/individual).

Базовое окружение в **environment.yml**. Для установки в терминале ввести:

`conda env create -f environment.yml`


Если нужно доставить новые пакеты из pip, заносите их в **environment.yml** по аналогии.

Чтобы обновить окружение:

`conda env update -f environment.yml`

`conda env update -f environment.yml --prune` - также удалит зависимости, которых больше нет в конфиге.

