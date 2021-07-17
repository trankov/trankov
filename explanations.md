# Собрать данные о людях

## Формулировка ТЗ

> Для сбора данных нужно сделать скрипт получения данных всех страниц людей с российской и английской википедии со следующими данными:
>
>- id
>- Ссылка на страницу в Википедии
>- Ссылка на фото
>- Пол
>- Фамилия
>- Имя
>- Отчество, если есть
>- Гражданство, какой страны
>- Дата рождения
>- Страна рождения
>- Регион, Область, Штат рождения
>- Город рождения
>- Дата смерти, если человек не умер, оставить поле пустым
>- Страна смерти
>- Регион / Область / Штат смерти
>- Город смерти
>- Род деятельности / профессия. Каждую профессию вынести в отдельный столбец и напротив человека, если относится к профессии ставить 1, если не относится, то 0.
>- Кол-во просмотров за каждый год с 2015 по 2020
>- Кол-во просмотров страниц человека за каждый месяц с 2020 года по июнь 2021
> Пример файла с выгрузкой [LINK](https://docs.google.com/spreadsheets/d/1CwZAFeFtuq)
>
> Данные нужно собирать из категории human (человек), идентификатор такой wd:Q5 wdt:P31. [LINK](https://query.wikidata.org/#SELECT%20%3Fperson%20WHERE%20%7B%20%3Fperson%20wdt%3AP31%20wd%3AQ5%20%7D%0Alimit%20100)
>
> Результат:
> Скрипт получения данных, с инструкцией развертывания и запуска.
> По два файла форматов sql. и .xlsx с выгрузками с российской и английской википедии. В выгрузке людей отсортировать по кол-ву просмотров за 2020 год, от большего к меньшему . Всего страниц людей будет больше 9 млн [LINK](https://www.wikidata.org/w/index.php?search=haswbstatement%3A%22P31%3DQ5%22&title=Special:Search&profile=advanced&fulltext=1&ns0=1&ns120=1). Для .xlsx разбить файлы на несколько частей, чтобы открылись для анализа в Excel.

Данное ТЗ было частично изменено в процессе обсуждения по ходу выполнения задачи.

## Вступление

Для выполнения задачи нужно выполнить две подзадачи.

1. Получить данные о людях, упомянутых в вики-проектах (викиданные, Wikidata).
2. Получить данные о статистике посещений статей в Википедии об этих людях (Wikipedia article).

## Данные о людях

Не о каждом человеке из Викиданных есть статья в Википедии.
То есть не для каждого найденного человека будет доступна статистика.

Данные о людях мы получаем с сервиса
```http
https://query.wikidata.org/
```

Для выполнения запросов используется язык SPARQL. Вкратце, он создан для обмена данными между разными проектами на основе кодирования свойств этих данных. Напоминает обычный SQL, но вместо полей и таблиц — сущности и типы связей между ними.


Мы отправляем запрос по адресу
```http
https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=
```
 и получаем json-ответ (или не получаем). Если запрос выполнился частично и в ходе возникла ошибка, ее описание придет хвостом к результатам запроса.

### Построение запроса
Синтаксис похож на SQL:
```sql
SELECT имена_переменных, через запятую
WHERE { условия }
LIMIT 0 OFFSET 0 GROUP BY...
```
### Работающий запрос, удовлетворяющий ТЗ:

```sql
PREFIX schema: <http://schema.org/>

SELECT ?human ?humanLabel
       ?image
       ?article
       (GROUP_CONCAT(DISTINCT ?sex_or_genderLabel;separator=", ") as ?sexgender)
       (GROUP_CONCAT(DISTINCT ?given_nameLabel;separator=", ") as ?namegiven)
       (GROUP_CONCAT(DISTINCT ?nameLabel;separator=", ") as ?nameitself)
       (GROUP_CONCAT(DISTINCT ?official_nameLabel;separator=", ") as ?nameofficial)
       (GROUP_CONCAT(DISTINCT ?family_nameLabel;separator=", ") as ?famname)
       ?date_of_birthLabel
       (GROUP_CONCAT(DISTINCT ?place_of_birthLabel;separator=", ") as ?birthplace)
       (GROUP_CONCAT(DISTINCT ?countrybirthLabel;separator=", ") as ?birthcountry)
       (GROUP_CONCAT(DISTINCT ?statebirthLabel;separator=", ") as ?birthstate)
       ?birthdayLabel
       (GROUP_CONCAT(DISTINCT ?country_of_citizenshipLabel;separator=", ") as ?citizenship)
       ?date_of_deathLabel
       (GROUP_CONCAT(DISTINCT ?place_of_deathLabel;separator=", ") as ?deathplace)
       (GROUP_CONCAT(DISTINCT ?countrydeathLabel;separator=", ") as ?deathcountry)
       (GROUP_CONCAT(DISTINCT ?statedeathLabel;separator=", ") as ?deathstate)
       (GROUP_CONCAT(DISTINCT ?occupationLabel;separator=", ") as ?occupazione)

WHERE
{
  {
    SELECT ?human ?article WHERE
      {
      ?human wdt:P31 wd:Q5.
        ?article schema:about ?human.
        ?article schema:inLanguage "en".
        ?article schema:isPartOf <https://en.wikipedia.org/>.
      }
    OFFSET 5000
    LIMIT 10
  }

  OPTIONAL { ?human wdt:P18 ?image. }
  OPTIONAL { ?human wdt:P21 ?sex_or_gender. }
  OPTIONAL { ?human wdt:P735 ?given_name. }
  OPTIONAL { ?human wdt:P2561 ?name. }
  OPTIONAL { ?human wdt:P1448 ?official_name. }
  OPTIONAL { ?human wdt:P734 ?family_name. }
  OPTIONAL { ?human wdt:P569 ?date_of_birth. }
  OPTIONAL { ?human wdt:P19 ?place_of_birth. }
  OPTIONAL { ?human wdt:P19/wdt:P17+ ?countrybirth. }
  OPTIONAL { ?human wdt:P19/wdt:P131+ ?statebirth. }
  OPTIONAL { ?human wdt:P3150 ?birthday. }
  OPTIONAL { ?human wdt:P27 ?country_of_citizenship. }
  OPTIONAL { ?human wdt:P570 ?date_of_death. }
  OPTIONAL { ?human wdt:P20 ?place_of_death. }
  OPTIONAL { ?human wdt:P20/wdt:P17+ ?countrydeath. }
  OPTIONAL { ?human wdt:P20/wdt:P131+ ?statedeath. }
  OPTIONAL { ?human wdt:P106 ?occupation. }



  SERVICE wikibase:label { bd:serviceParam wikibase:language "en".

                           ?human rdfs:label ?humanLabel.
                           ?date_of_birth rdfs:label ?date_of_birthLabel.
                           ?date_of_death rdfs:label ?date_of_deathLabel.
                           ?birthday rdfs:label ?birthdayLabel.
                           ?sex_or_gender rdfs:label ?sex_or_genderLabel.
                           ?given_name rdfs:label ?given_nameLabel.
                           ?name rdfs:label ?nameLabel.
                           ?official_name rdfs:label ?official_nameLabel.
                           ?family_name rdfs:label ?family_nameLabel.
                           ?place_of_birth rdfs:label ?place_of_birthLabel.
                           ?statebirth rdfs:label ?statebirthLabel.
                           ?countrybirth rdfs:label ?countrybirthLabel.
                           ?country_of_citizenship rdfs:label ?country_of_citizenshipLabel.
                           ?place_of_death rdfs:label ?place_of_deathLabel.
                           ?countrydeath rdfs:label ?countrydeathLabel.
                           ?statedeath rdfs:label ?statedeathLabel.
                           ?occupation rdfs:label ?occupationLabel.
                         }
}
GROUP BY
       ?human ?humanLabel
       ?article
       ?image
       ?date_of_birthLabel
       ?birthdayLabel
       ?date_of_deathLabel
```

Для получения записей на русском языке все определения `en` надо заменить на `ru`. Параметры `OFFSET` и `LIMIT` меняются по необходимости.

Запрос структурно усложнён из-за того, что разбит на 2 инструкции SELECT вместо одного. Так сделано исходя из [официальных рекомендаций Wikimedia](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/query_optimization). Кроме того, весь запрос построен с их учётом.

**Этот запрос работает и отдаёт результаты в нужном виде, если параметры `LIMIT` и `OFFSET` выставлены удачно**.

Пример ответа при `LIMIT 5` и `OFFSET 0`:

```json
{
    "head": {
        "vars": [
            "human",
            "humanLabel",
            "image",
            "article",
            "sexgender",
            "namegiven",
            "nameitself",
            "nameofficial",
            "famname",
            "date_of_birthLabel",
            "birthplace",
            "birthcountry",
            "birthstate",
            "birthdayLabel",
            "citizenship",
            "date_of_deathLabel",
            "deathplace",
            "deathcountry",
            "deathstate",
            "occupazione"
        ]
    },
    "results": {
        "bindings": [
            {
                "human": { "type": "uri", "value": "http://www.wikidata.org/entity/Q297" },
                "humanLabel": { "xml:lang": "en", "type": "literal", "value": "Diego Velázquez" },
                "article": { "type": "uri", "value": "https://en.wikipedia.org/wiki/Diego_Vel%C3%A1zquez" },
                "image": {
                    "type": "uri",
                    "value": "http://commons.wikimedia.org/wiki/Special:FilePath/Diego%20Vel%C3%A1zquez%20Autorretrato%2045%20x%2038%20cm%20-%20Colecci%C3%B3n%20Real%20Academia%20de%20Bellas%20Artes%20de%20San%20Carlos%20-%20Museo%20de%20Bellas%20Artes%20de%20Valencia.jpg"
                },
                "date_of_birthLabel": { "type": "literal", "value": "1599-06-06T00:00:00Z" },
                "date_of_deathLabel": { "type": "literal", "value": "1660-08-06T00:00:00Z" },
                "sexgender": { "type": "literal", "value": "male" },
                "namegiven": { "type": "literal", "value": "Diego" },
                "nameitself": { "type": "literal", "value": "" },
                "nameofficial": { "type": "literal", "value": "" },
                "famname": { "type": "literal", "value": "Velázquez" },
                "birthplace": { "type": "literal", "value": "Seville" },
                "birthcountry": { "type": "literal", "value": "Spain" },
                "birthstate": {
                    "type": "literal",
                    "value": "Seville Province, Kingdom of Seville, Comarca Metropolitana de Sevilla, Andalusia, Spain"
                },
                "citizenship": { "type": "literal", "value": "Spain" },
                "deathplace": { "type": "literal", "value": "Madrid" },
                "deathcountry": { "type": "literal", "value": "Spain" },
                "deathstate": { "type": "literal", "value": "Community of Madrid, Spain" },
                "occupazione": { "type": "literal", "value": "painter" }
            },
            {
                "human": { "type": "uri", "value": "http://www.wikidata.org/entity/Q368" },
                "humanLabel": { "xml:lang": "en", "type": "literal", "value": "Augusto Pinochet" },
                "article": { "type": "uri", "value": "https://en.wikipedia.org/wiki/Augusto_Pinochet" },
                "image": {
                    "type": "uri",
                    "value": "http://commons.wikimedia.org/wiki/Special:FilePath/Augusto%20Pinochet%20-%201995.jpg"
                },
                "date_of_birthLabel": { "type": "literal", "value": "1915-11-25T00:00:00Z" },
                "date_of_deathLabel": { "type": "literal", "value": "2006-12-10T00:00:00Z" },
                "sexgender": { "type": "literal", "value": "male" },
                "namegiven": { "type": "literal", "value": "Augusto, Ramón, José" },
                "nameitself": { "type": "literal", "value": "" },
                "nameofficial": { "type": "literal", "value": "" },
                "famname": { "type": "literal", "value": "Pinochet" },
                "birthplace": { "type": "literal", "value": "Valparaíso" },
                "birthcountry": { "type": "literal", "value": "Chile" },
                "birthstate": {
                    "type": "literal",
                    "value": "Valparaíso, Valparaíso Province, Valparaíso Region, Chile"
                },
                "citizenship": { "type": "literal", "value": "Chile" },
                "deathplace": { "type": "literal", "value": "Santiago" },
                "deathcountry": { "type": "literal", "value": "Chile" },
                "deathstate": { "type": "literal", "value": "Santiago Metropolitan Region, Chile" },
                "occupazione": { "type": "literal", "value": "politician, military officer" }
            },
            {
                "human": { "type": "uri", "value": "http://www.wikidata.org/entity/Q207" },
                "humanLabel": { "xml:lang": "en", "type": "literal", "value": "George W. Bush" },
                "article": { "type": "uri", "value": "https://en.wikipedia.org/wiki/George_W._Bush" },
                "image": {
                    "type": "uri",
                    "value": "http://commons.wikimedia.org/wiki/Special:FilePath/George-W-Bush.jpeg"
                },
                "date_of_birthLabel": { "type": "literal", "value": "1946-07-06T00:00:00Z" },
                "sexgender": { "type": "literal", "value": "male" },
                "namegiven": { "type": "literal", "value": "George" },
                "nameitself": { "type": "literal", "value": "" },
                "nameofficial": { "type": "literal", "value": "" },
                "famname": { "type": "literal", "value": "Bush" },
                "birthplace": { "type": "literal", "value": "New Haven" },
                "birthcountry": { "type": "literal", "value": "United States of America" },
                "birthstate": { "type": "literal", "value": "New Haven County, Connecticut, United States of America" },
                "citizenship": { "type": "literal", "value": "United States of America" },
                "deathplace": { "type": "literal", "value": "" },
                "deathcountry": { "type": "literal", "value": "" },
                "deathstate": { "type": "literal", "value": "" },
                "occupazione": { "type": "literal", "value": "politician, statesperson" }
            },
            {
                "human": { "type": "uri", "value": "http://www.wikidata.org/entity/Q873" },
                "humanLabel": { "xml:lang": "en", "type": "literal", "value": "Meryl Streep" },
                "article": { "type": "uri", "value": "https://en.wikipedia.org/wiki/Meryl_Streep" },
                "image": {
                    "type": "uri",
                    "value": "http://commons.wikimedia.org/wiki/Special:FilePath/Meryl%20Streep%20December%202018.jpg"
                },
                "date_of_birthLabel": { "type": "literal", "value": "1949-06-22T00:00:00Z" },
                "sexgender": { "type": "literal", "value": "female" },
                "namegiven": { "type": "literal", "value": "Mary, Louise" },
                "nameitself": { "type": "literal", "value": "" },
                "nameofficial": { "type": "literal", "value": "" },
                "famname": { "type": "literal", "value": "Streep" },
                "birthplace": { "type": "literal", "value": "Summit" },
                "birthcountry": { "type": "literal", "value": "United States of America" },
                "birthstate": { "type": "literal", "value": "Union County, New Jersey, United States of America" },
                "citizenship": { "type": "literal", "value": "United States of America" },
                "deathplace": { "type": "literal", "value": "" },
                "deathcountry": { "type": "literal", "value": "" },
                "deathstate": { "type": "literal", "value": "" },
                "occupazione": {
                    "type": "literal",
                    "value": "actor, television producer, stage actor, voice actor, film producer, television actor, film actor"
                }
            },
            {
                "human": { "type": "uri", "value": "http://www.wikidata.org/entity/Q501" },
                "humanLabel": { "xml:lang": "en", "type": "literal", "value": "Charles Baudelaire" },
                "article": { "type": "uri", "value": "https://en.wikipedia.org/wiki/Charles_Baudelaire" },
                "image": {
                    "type": "uri",
                    "value": "http://commons.wikimedia.org/wiki/Special:FilePath/Baudelaire%20crop.jpg"
                },
                "date_of_birthLabel": { "type": "literal", "value": "1821-04-09T00:00:00Z" },
                "date_of_deathLabel": { "type": "literal", "value": "1867-08-30T00:00:00Z" },
                "sexgender": { "type": "literal", "value": "male" },
                "namegiven": { "type": "literal", "value": "Pierre, Charles" },
                "nameitself": { "type": "literal", "value": "" },
                "nameofficial": { "type": "literal", "value": "" },
                "famname": { "type": "literal", "value": "Baudelaire" },
                "birthplace": { "type": "literal", "value": "Paris" },
                "birthcountry": { "type": "literal", "value": "France" },
                "birthstate": {
                    "type": "literal",
                    "value": "Metropolis of Greater Paris, Île-de-France, France, Metropolitan France, Q88521107"
                },
                "citizenship": { "type": "literal", "value": "France" },
                "deathplace": { "type": "literal", "value": "Paris" },
                "deathcountry": { "type": "literal", "value": "France" },
                "deathstate": {
                    "type": "literal",
                    "value": "Metropolis of Greater Paris, Île-de-France, France, Metropolitan France, Q88521107"
                },
                "occupazione": {
                    "type": "literal",
                    "value": "writer, poet, translator, author, art critic, literary critic, essayist"
                }
            },
            {
                "human": { "type": "uri", "value": "http://www.wikidata.org/entity/Q853" },
                "humanLabel": { "xml:lang": "en", "type": "literal", "value": "Andrei Tarkovsky" },
                "article": { "type": "uri", "value": "https://en.wikipedia.org/wiki/Andrei_Tarkovsky" },
                "image": {
                    "type": "uri",
                    "value": "http://commons.wikimedia.org/wiki/Special:FilePath/Andrei%20tarkovsky%20stamp%20russia%202007.jpg"
                },
                "date_of_birthLabel": { "type": "literal", "value": "1932-04-04T00:00:00Z" },
                "date_of_deathLabel": { "type": "literal", "value": "1986-12-29T00:00:00Z" },
                "sexgender": { "type": "literal", "value": "male" },
                "namegiven": { "type": "literal", "value": "Andrei" },
                "nameitself": { "type": "literal", "value": "" },
                "nameofficial": { "type": "literal", "value": "" },
                "famname": { "type": "literal", "value": "Tarkovsky" },
                "birthplace": { "type": "literal", "value": "Zavrazhye" },
                "birthcountry": { "type": "literal", "value": "Russia" },
                "birthstate": { "type": "literal", "value": "Q19836427, Kadyysky District, Kostroma Oblast, Russia" },
                "citizenship": { "type": "literal", "value": "Soviet Union" },
                "deathplace": { "type": "literal", "value": "Paris" },
                "deathcountry": { "type": "literal", "value": "France" },
                "deathstate": {
                    "type": "literal",
                    "value": "Metropolis of Greater Paris, Île-de-France, France, Metropolitan France, Q88521107"
                },
                "occupazione": {
                    "type": "literal",
                    "value": "screenwriter, actor, biographer, film director, theatrical director, director, film editor, film actor"
                }
            }
        ]
    }
}
```

К сожалению, на определённом шаге смещения начинает стабильно возвращаться `TimeoutError`.

Попытки как-то упростить запрос не привели к работающим результатам. Не удалось победить проблему `TimeoutError` на сколь бы то ни было приемлемых условиях.

### Итог

Удалось стабильно получить набор записей вида `[wd:, label]`, где wd это идентификатор, а label имя объекта, совпадающее с названием статьи в Wikipedia, если она есть.

См. скрипт получения данных и комментарии в файле `reader.py`

## Получение данных о посещении страниц

За получение данных о странице отвечает специальный [Wikimedia REST API](https://wikimedia.org/api/rest_v1/#/Pageviews%20data/get_metrics_pageviews_per_article__project___access___agent___article___granularity___start___end_).

Там всё очень просто и не нужно ничего выдумывать, кроме того, как получать данные для формирования запросов и куда их сохранять. У нас 9,2 млн. записей, это очень много.

Для быстрого чтения данных была создана база данных PostgreSQL. Импорт в неё осуществлялся из заранее подготовленного CSV-файла командой `COPY FROM`. Процедура импорта занимает около 80 секунд.

CSV-файл из набора .json-файлов формирует скрипт `csv_formatter.py`. Время его работы зависит от среды исполнения (от 20 до 40 минут).

Чтение из базы, формирование запросов и запись результатов в CSV осуществляет скрипт `benchmark.py`.

Все скрипты соблюдают ограничения по нагрузке на Wikimedia API и соответствуют их требованиям к формированию запросов.

CSV-файл со статистикой посещений тоже потом может быть загружен в PostgreSQL для дальнейшей обработки, если понадобится.

## Передаваемые материалы
### Файлы с рабочими результатами
Эти файлы являются результатом проверки работы запросов и могут (желательно) быть переформированы заново согласно инструкциям в скриптах.

| Файл               | Описание           |
| ------------------ | ------------------ |
| `json_en.zip`        | Результаты запросов к Wikidata |
| `json_ru.tar.bz`     | То же для русского языка |
| `biglist-en.csv.bz2` | Cтатистикой посещений Wikipedia
| `biglist-ru.csv.bz2` | То же для русского языка

### Файлы со скриптами
Скрипты написаны на языке Python 3.9, см. доп. инструкцию в конце документа. Все комментарии в коде написаны на русском языке.

| Файл               | Описание           |
| ------------------ | ------------------ |
| `reader.py` | Пошагово отправляет запросы к Wikidata и сохраняет промежуточные результаты в отдельных файлах |
| `csv_formatter.py`   | Формирует CSV из загруженных результатов для дальнейшего импорта в базу данных |
| `benchmark.py` | Получает данные о людях из базы и асинхронно отправляет запросы к Wikimedia REST API. Результат сохраняет в CSV. |
| `requirements.txt` | Файл с зависимостями для скриптов |

## Настройка окружения
На Маке
```shell
$ brew install python@3.9
```
На Windows скачать и установить дистрибутив c python.org

После установки (опционально, но рекомендуется) можно создать виртуальное окружение, но будет работать и без него

```shell
$ cd нужная_директория
$ python3 -m venv wikidata
$ cd wikidata
$ . bin/activate
```
На Windows вместо `. bin/activate` пишется `Scripts\activate.bat`.

Далее нужно установить зависимости (библиотеки) для работы скриптов. Для этого в каталоге **wikidata** должен быть файл `requirements.txt`. Далее запускаем менеджер зависимостей и ждём окончания установки.

```shell
$ pip3 install -r requirements.txt
```

Скрипты запускаются командой

```shell
$ python3 путь-к-файлу/скрипт.py
```

Если у вас запущено виртуальное окружение, путь к файлу можно не писать:

```shell
(wikidata)$ python filename.py
```
Не забывайте выполнять
```shell
$. bin/activate
```
каждый раз, когда заново начинаете работать. По окончании работы отключите виртуальное окружение командой

```shell
$ deactivate
```
