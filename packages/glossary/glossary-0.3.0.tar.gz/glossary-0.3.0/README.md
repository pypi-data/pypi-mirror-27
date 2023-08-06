Сервис/клиентская либа для общих данных в ЭИОС (Ионосфера).

# Локальная разработка

По ссылке `/client-admin/` есть админка, которая будет у

клиентского приложения. Ее можно использовать для тестов.

# Установка

* `pip install glossary`
* Добавьте `glossary` в `INSTALLED_APPS`
* Примените миграции - `./manage.py migrate`
* Укажите адрес сервиса (`GLOSSARY_SERVICE_URL = "http://glossary.dissw.ru"`, например)
* Добавьте URL'ы глоссария в urlconf:

``` python
urlpatterns = [
    ...,
    url(r"glossary/",·include("glossary.urls")),
    ...
```
* `./manage.py register http://<IP, название сервиса в docker-compose или доменное имя>`
* Сделайте, что напишет команда