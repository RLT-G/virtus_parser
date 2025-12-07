# DRF API virtus_parser

---

## 1. Общее описание проекта

DRF-проект представляет собой **REST API** для работы с данными **HLTV.org**, предоставляя:
* Профили команд и игроков
* Матчи команд
* Статистику игроков
* Предстоящие и прошедшие матчи
* Tableau CSV-данные (CT-side / T-side)

Проект использует:
* Django 4.x
* Django REST Framework
* drf-spectacular для OpenAPI/Swagger документации
* Внутренний модуль HLTVScraper для получения данных
* Локальные CSV файлы для таблиц стратегии (tableau/)

---

## 2. Структура проекта
```
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── hltv_scraper
│   │   ├── cache_config.py
│   │   ├── cleaner.py
│   │   ├── conditions_checker.py
│   │   ├── conditions_factory.py
│   │   ├── conditions.py
│   │   ├── data
│   │   ├── data.py
│   │   ├── hltv_scraper
│   │   ├── __init__.py
│   │   ├── path_generator.py
│   │   ├── process.py
│   │   ├── scrapy.cfg
│   │   └── spider_manager.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tableau
│   │   ├── ct_side.csv
│   │   └── t_side.csv
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── doc.txt
├── Makefile
├── manage.py
├── requirements.txt
└── settings
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

---

## 3. API Endpoints

---

#### 3.1 Системные
| Endpoint        | Method | Описание                 | Request | Response          |
| --------------- | ------ | ------------------------ | ------- | ----------------- |
| `/api/v1/check` | GET    | Проверка доступности API | нет     | `{"status":"ok"}` |

---
#### 3.2 Команды (Team)
| Endpoint               | Method | Описание                         | Request | Response                               |
| ---------------------- | ------ | -------------------------------- | ------- | -------------------------------------- |
| `/api/v1/team/info`    | POST   | Возвращает информацию о команде  | None    | `{"status":"ok","team_info":{...}}`    |
| `/api/v1/team/matches` | POST   | Возвращает список матчей команды | None    | `{"status":"ok","team_matches":[...]}` |

---

#### 3.3 Игроки (Player)
| Endpoint                    | Method | Описание                   | Request                        | Response                                 |
| --------------------------- | ------ | -------------------------- | ------------------------------ | ---------------------------------------- |
| `/api/v1/player/search`     | POST   | Поиск игрока по имени      | `{"name":"FL1T"}`              | `{"status":"ok","player":{...}}`         |
| `/api/v1/player/profile`    | POST   | Получение профиля игрока   | `{"name":"FL1T","id":"12732"}` | `{"status":"ok","player_profile":{...}}` |
| `/api/v1/player/statistics` | POST   | Overview статистика игрока | `{"name":"FL1T","id":"12732"}` | `{"status":"ok","player_stat":{...}}`    |

---

#### 3.4 Матчи (Matches)
| Endpoint                   | Method | Описание                   | Request                                                            | Response                                   |
| -------------------------- | ------ | -------------------------- | ------------------------------------------------------------------ | ------------------------------------------ |
| `/api/v1/matches/upcoming` | POST   | Возвращает ближайшие матчи | None                                                               | `{"status":"ok","upcoming_matches":[...]}` |
| `/api/v1/matches/details`  | POST   | Детали матча               | `{"id":"2372341","match_name":"virtuspro-vs-big-iem-dallas-2024"}` | `{"status":"ok","match_details":{...}}`    |

---

#### 3.5 Tableau данные (CT-side / T-side)
| Endpoint                 | Method | Описание                                    | Request | Response                         |
| ------------------------ | ------ | ------------------------------------------- | ------- | -------------------------------- |
| `/api/v1/tableau/ctside` | POST   | Чтение ct_side.csv и возврат как list[dict] | None    | `{"status":"ok","t_side":[...]}` |
| `/api/v1/tableau/tside`  | POST   | Чтение t_side.csv и возврат как list[dict]  | None    | `{"status":"ok","t_side":[...]}` |

---

## 4. Описание работы с HLTVScraper

---

#### Общее описание

`HLTVScraper` — это Python-модуль, предназначенный для парсинга сайта HLTV.org и получения актуальных данных о CS:GO матчах, командах и игроках.

Модуль реализован как асинхронный Scrapy-краулер с кэшированием JSON, который обеспечивает:

* получение профилей команд и игроков,
* поиск игроков и команд,
* получение статистики игроков,
* получение предстоящих матчей, результатов и новостей,
* хранение всех данных в локальном файловом кэше с TTL (время жизни).

---

#### Технологии и библиотеки

Модуль использует:

* Python 3.10+
* Scrapy — основной фреймворк для веб-скрейпинга.
* Cloudscraper — для обхода защиты Cloudflare при запросах к HLTV.
* JSON — для хранения данных локально.
* Файловая система — для кэша и локальных данных (data/).
* ABC и typing — для строгой типизации и абстрактных интерфейсов.
* Стандартные библиотеки: os, time, datetime, subprocess.

---

#### Архитектура модуля HLTVScraper

---


1. **HLTVScraper (API)**
	* Основной класс для работы с внешними методами.
	* Все методы статические.
	* Методы возвращают dict, загружая данные из JSON или запуская Scrapy-спайдеры при необходимости.
	* Методы включают:

| Категория  | Метод                                        | Описание                                |
| ---------- | -------------------------------------------- | --------------------------------------- |
| Матчи      | `get_upcoming_matches()`                     | Получение списка предстоящих матчей     |
| Матчи      | `get_match(id, match_name)`                  | Получение информации о конкретном матче |
| Команды    | `get_team_rankings()`                        | Получение рейтинга команд               |
| Команды    | `search_team(name)`                          | Поиск команды по имени                  |
| Команды    | `get_team_matches(id, offset)`               | Получение матчей команды                |
| Команды    | `get_team_profile(id, team_name)`            | Получение профиля команды               |
| Игроки     | `search_player(name)`                        | Поиск игрока по имени                   |
| Игроки     | `get_player_profile(id, player_name)`        | Получение профиля игрока                |
| Игроки     | `get_player_stats_overview(id, player_name)` | Получение статистики игрока             |
| Результаты | `get_results(offset)`                        | Получение всех результатов              |
| Результаты | `get_big_results()`                          | Получение значимых результатов          |
| Новости    | `get_news(year, month)`                      | Получение новостей по месяцам           |

**Особенности работы:**
* Все методы используют SpiderManager для запуска Scrapy-пауков и проверки кэша.
* Если JSON-файл свежий — данные берутся из него.
* Если JSON отсутствует или устарел — запускается соответствующий Scrapy-спайдер.

---

2. **SpiderManager**
	Отвечает за **логическую работу с пауками, условиями и кэшем**.
	
	Основные функции:
	
	* Проверка условий запуска спайдера (`__should_run__`) (Если хотя бы одно условие выполняется → запускается спайдер)
	* Запуск спайдера (`run_spider`):
	* Получение результата (`get_result`):
	* Профили команд и игроков (`get_profile`, `is_profile`):

---

3. **Кэширование**
	* Все данные хранятся в папке `data/` внутри структуры `hltv_scraper`.
	- Время жизни кэша определяется в `cache_config.py`

| Тип данных        | Время жизни (часы) |
| ----------------- | ------------------ |
| Новости           | 24                 |
| Матчи             | 1                  |
| Результаты        | 1                  |
| Команды           | 24                 |
| Игроки            | 24                 |
| Рейтинги          | 12                 |
| Предстоящие матчи | 1                  |
| Матчи команды     | 1                  |
| Важные результаты | 1                  |
| Статистика игрока | 24                 |

---

4. **Scrapy-спайдеры**
	* Каждый спайдер отвечает за отдельную сущность (игрок, команда, матч, рейтинг).
	* Пример: HltvMatchSpider:
		* Получает URL вида `https://www.hltv.org/matches/{match}`.
		* Использует cloudscraper для обхода Cloudflare.
		* Парсит HTML с помощью ParsersFactory.
		* Возвращает словарь с командами, картами и статистикой.
	* Другие спайдеры работают аналогично (hltv_team.py, hltv_players_search.py, hltv_team_matches.py и т.д.).

---

5. **Парсеры**
	- Содержатся в `parsers/`.
	- Все спайдеры используют `ParsersFactory` для получения нужного парсера.
	- Примеры:
	    - `match_teams_box` — парсит информацию о командах в матче.
	    - `table_stats` — парсит статистику игроков        
	    - `team_profile` — парсит профиль команды.
	    - `player_profile_link` — парсит ссылки на игроков.
	    - `players_profile` — формирует структуру JSON с данными игрока.
	- Парсеры разделяют:
	    - HTML-селекторы (`response.css`)
	    - Логику обработки и нормализации данных
	    - Подготовку к сохранению в JSON

---

6. **Файловая структура кэша**

```
data/
├─ match/{id}_{match_name}.json
├─ player/{player_name}.json
├─ players_profiles.json
├─ player_stats_overview/{player_name}.json
├─ team/{team_name}.json
├─ team_matches/{id}_{offset}.json
├─ upcoming_matches.json
```

- Каждая сущность сохраняется отдельно.
- Обеспечивает быстрый доступ и минимизирует повторные запросы к HLTV.

---

7. **Работа с JSON**

- Используется `JsonDataLoader` (data.py).
- При ошибках чтения JSON возвращает пустой `dict`.
- `JsonOldDataCleaner` очищает файлы перед повторным запуском спайдера.

---

8. **Процесс запуска Scrapy**

- `SpiderProcess.execute()` использует `subprocess.Popen`:

 ```python
  ["scrapy", "crawl", spider_name] + args.split()
  ```

- Пауки запускаются в рабочей директории `hltv_scraper`.
- Используется стандартный Scrapy pipeline (`HltvScraperPipeline`) — пока просто возвращает item без изменений.

---

## 5. Интеграция HLTVScraper с Django DRF

- `HLTVScraper` используется во внешнем DRF API.
- Пример методов:

```python
def search_player(name: str):
    """Search player by name from HLTV"""
    data = HLTVScraper.search_player(name)
    return data 

def get_player_profile(id: str, player_name: str):
    """Get player profile from HLTV."""
    data = HLTVScraper.get_player_profile(id, player_name)
    return data

def get_player_stats_overview(id: str, player_name: str):
    """Get player statistics overview from HLTV."""
    data = HLTVScraper.get_player_stats_overview(id, player_name)
    return data
```

- API работает через POST-запросы и возвращает JSON.
- Все запросы к HLTV проходят через Scrapy + локальный кэш.

---

## 6. Механизм работы запросов

1. **Команды и игроки:**
    - Все запросы используют `utils.py`, который вызывает HLTVScraper.
    - JSON кэш хранится в `hltv_scraper/data`.
    - Если данные устарели → запускается Scrapy-паук.
        
2. **Матчи:**
    - `/matches/upcoming` → ближайшие матчи.
    - `/matches/details` → детальные данные по HLTV id и slug матча.
        
3. **Tableau:**
    - CSV файлы читаются через `csv_to_dict_from_path`.
    - Поддерживаются различные кодировки: utf-8, utf-16, utf-16-be, utf-8-sig.
        
4. **Обработка ошибок:**
    - При некорректных данных возвращается `400 Bad Request`.
    - При внутренних ошибках HLTVScraper или utils → `500 Internal Server Error`.
    - Все успешные ответы имеют ключ `"status": "ok"`.

---

## 7. Swagger/OpenAPI документация

- `/api/v1/schema` → JSON OpenAPI схема
- `/api/v1/swagger` → Swagger UI для визуальной работы с API
- Документация генерируется с помощью **drf-spectacular** и `@extend_schema`.

---

## 8. Примеры использования (curl + jq)

```bash
# Проверка работы API
curl http://127.0.0.1:8080/api/v1/check | jq

# Команды
curl -X POST http://127.0.0.1:8080/api/v1/team/info | jq
curl -X POST http://127.0.0.1:8080/api/v1/team/matches | jq

# Игроки
curl -X POST http://127.0.0.1:8080/api/v1/player/search --json '{"name":"FL1T"}' | jq
curl -X POST http://127.0.0.1:8080/api/v1/player/profile --json '{"name":"FL1T", "id":"12732"}' | jq
curl -X POST http://127.0.0.1:8080/api/v1/player/statistics --json '{"name":"FL1T", "id":"12732"}' | jq

# Матчи
curl -X POST http://127.0.0.1:8080/api/v1/matches/upcoming | jq
curl -X POST http://127.0.0.1:8080/api/v1/matches/details --json '{"id":"2372341","match_name":"virtuspro-vs-big-iem-dallas-2024"}' | jq

# Tableau
curl -X POST http://127.0.0.1:8080/api/v1/tableau/ctside | jq
curl -X POST http://127.0.0.1:8080/api/v1/tableau/tside | jq
```

---

## 9. Взаимодействие с HLTVScraper

* Все основные API-вызовы внутри DRF проекта используют HLTVScraper через функции utils.py.
* API фактически является оберткой поверх HLTVScraper, добавляя:
	* REST интерфейс
	* Обработку ошибок
	* Swagger документацию
	* Единый формат JSON-ответов

---

## 10. Итоги

DRF-проект представляет собой полнофункциональный REST API для работы с данными HLTV.org. Его ключевые особенности:

1. **Удобный REST-интерфейс**
    - Все данные, включая информацию о командах, игроках, матчах и статистику, доступны через простые POST/GET запросы.
    - Swagger/OpenAPI документация позволяет легко тестировать и интегрировать API.
        
2. **Интеграция с HLTVScraper**
    - Все данные собираются и обновляются через Scrapy-пауки, реализованные в модуле HLTVScraper.
    - DRF проект выступает как «обертка», упрощая работу с HLTVScraper для внешних систем.
    - Механизм кэширования и проверка условий (файловое время, пустой JSON, наличие файла) позволяют оптимизировать количество запросов к HLTV.
        
3. **Обработка ошибок и надежность**
    - Некорректные запросы получают `400 Bad Request`.
    - Проблемы внутри HLTVScraper или utils фиксируются через `500 Internal Server Error`.
    - Все успешные ответы стандартизированы через `"status":"ok"`.
        
4. **Гибкость и расширяемость**
    - Модульная структура: utils, views, HLTVScraper, tableau данные.
    - Легко добавлять новые ручки, новые данные или расширять Scrapy-пауки для других видов информации.
        
5. **Практическое применение**
    - Этот API можно использовать для статистических дашбордов, аналитики команд и игроков, прогнозов матчей, интеграции с внутренними системами и внешними сервисами.
    - Tableau CSV позволяет подключать стратегические данные для анализа CT/T сторон.
        

**Итог:** DRF-проект + HLTVScraper образует полностью функциональный и масштабируемый инструмент для работы с данными HLTV.org, предоставляя удобный REST API с кэшированием, надежной обработкой ошибок и готовыми структурами для аналитики.

---
