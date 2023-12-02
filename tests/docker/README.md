# Тесты для Python2 в Docker

## Ссылки

-   [A Docker Tutorial for Beginners](https://docker-curriculum.com/)
-   [Самый простой, полный и понятный туториал Docker для новичков](https://badtry.net/docker-tutorial-dlia-novichkov-rassmatrivaiem-docker-tak-iesli-by-on-byl-ighrovoi-pristavkoi/)
-   [Полное практическое руководство по Docker: с нуля до кластера на AWS](https://habr.com/ru/articles/310460/)

## Настройка Docker

[Скачать](https://www.docker.com/products/docker-engine) и установить Docker.

Добавить пользователя в группу для использования Docker, запустив командную строку администратора.

```bash
net localgroup
net user
net localgroup docker-users vit /add
net localgroup docker-users
```

Перелогиниться как 'vit', затем  в обычной командной строке (не админ!)

```bash
wsl --update
```

Запустить "Docker Desktop", затем создать образ

```bash
cd tests/docker
build.cmd
```

Запустить тесты из корневого каталога проекта.
Перед запуском убедиться, что на локальном диске в каталоге `tests` нет `.pyc` файлов.
Если есть, то их все нужно удалить.

```bash
cd ../../
docker-compose --file tests/docker/docker-compose.yml run py2
```

Очистка

```bash
docker ps -a
docker container prune

docker-compose stop
docker-compose rm
```
