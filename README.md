![](Logo.png)
# Search engine for parking spaces according to outdoor cameras 

Запуск сервера из корневой папки: `uvicorn server.main:app --reload`

Запуск всех тестов `pytest`

Запуск определенного теста `pytest test_crud_cam_park.py`

Для запуска необходимых сервисов (<i>MongoDB</i>) должен быть установлен <b>Docker</b> . Для запуска необходимых контейнеров `docker-compose up --build` (флаг `-d` чтоб не занимать терминал, если не нужен вывод информации с контейнера). Данные для инициализации лежат в `entry_points/mongo-init.js`, они создаются при первой инициализации <i>MongoDB</i>. Чтобы остановить и/или удалить контейнеры текущего `docker-compose.yml` нужно в терминале ввести `docker-compose down`. Чтобы перезапустить опять нужно ввести `docker-compose up --build` (`docker-compose down` + `docker-compose up` = mongo реинициализируется, те при добавлении новых данных в `entry_points/mongo-init.js` они будут в БД).

В проекте используются переменные окружения из .env. 
1. Копируется файл .env.sample в .env, в нем должны быть ОБЪЯВЛЕНЫ все нужные константы.
2. В .env нужно ОПРЕДЕЛИТЬ нужные константы, .env лежит в .gitignore, чтобы не светить константы.
3. Для загрузки всех переменных из .env в окружение: 
```python
rom dotenv import load_dotenv
load_dotenv()
```
 4. Для доступа к переменной VARIABLE:
 ```python
os.getenv('VARIABLE')
```
 
