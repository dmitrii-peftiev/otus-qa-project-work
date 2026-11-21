# Разработка автоматизированных UI и API тестов на примере Swag Labs и ReqRes с использованием Python

![Python](https://img.shields.io/badge/Python-3.12.7-blue?style=flat-square&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Framework-green?style=flat-square&logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Testing-45ba4b?style=flat-square&logo=playwright&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Report-yellowgreen?style=flat-square&logo=allurereport&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Infrastructure-2496ED?style=flat-square&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=flat-square&logo=jenkins&logoColor=white)

Проектная работа по курсу **Автоматизатор тестирования на Python** (OTUS).

## Покрытие тестами (38 тестов)

* **API-тесты (25 тестов для [ReqRes](https://reqres.in/)):**
    * CRUD-операции с пользователями (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), пагинация и проверка `404`.
    * Регистрация и авторизация (позитивные проверки и негативные кейсы с ошибкой `400`).
    * Получение списка ресурсов, одиночного ресурса и проверка задержки ответа.
* **UI-тесты (13 тестов для [Swag Labs](https://www.saucedemo.com/)):**
    * Авторизация (валидный пользователь, заблокированный пользователь, пустые поля и неверный пароль).
    * Сортировка товаров по цене и по алфавиту.
    * Добавление и удаление товара в корзине, оформление заказа (E2E), валидация формы покупателя и выход из системы
      (Logout).
    * Автоматическое прикрепление скриншота в Allure при падении UI-теста.

## Структура проекта

| Директория / Файл                              | Описание                                                                                                             |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------|
| **[`src/api`](./src/api)**                     | API-клиент и модели запросов для тестирования REST API                                                               |
| **[`src/pages`](./src/pages)**                 | PageObject-модели страниц для UI-тестирования (`BasePage`, `LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`) |
| **[`src/utils`](./src/utils)**                 | Конфигурация проекта (`config.py`) и генератор тестовых данных на базе Faker (`data_generator.py`)                   |
| **[`tests/api`](./tests/api)**                 | Автотесты для проверки REST API (маркер `@pytest.mark.api`)                                                          |
| **[`tests/ui`](./tests/ui)**                   | Автотесты для проверки пользовательского интерфейса (маркер `@pytest.mark.ui`)                                       |
| **[`tests/conftest.py`](./tests/conftest.py)** | Фикстуры Pytest (`api_client`, `browser`, `page`, `logged_in_page`) и хук снятия скриншота при падении               |
| **[`docker`](./docker)**                       | `Dockerfile` (Jenkins + Python + Playwright + Chromium) и `docker-compose.yml`                                       |
| **[`Jenkinsfile`](./Jenkinsfile)**             | Декларативный пайплайн CI/CD с выбором набора тестов (`all`, `ui`, `api`) и генерацией Allure-отчёта                 |
| **[`pytest.ini`](./pytest.ini)**               | Конфигурация Pytest, регистрация маркеров и директория результатов Allure                                            |
| **[`requirements.txt`](./requirements.txt)**   | Зависимости проекта                                                                                                  |

## Инструкции по развёртыванию и запуску

<details>
<summary><strong>Локальный запуск тестов</strong></summary>

### Подготовка окружения

1. Клонировать репозиторий и перейти в папку проекта:

```bash
git clone https://github.com/dmitrii-peftiev/otus-qa-project-work.git
```

```bash
cd otus-qa-project-work
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
```

* Windows:

```bash
.venv\Scripts\activate
```

* Linux / macOS:

```bash
source .venv/bin/activate
```

3. Установить зависимости и браузер Chromium:

```bash
pip install -r requirements.txt
```

```bash
playwright install chromium
```

4. При необходимости создать файл `.env` в корне проекта по образцу `.env.example`.

### Запуск автотестов

```bash
pytest
```

```bash
pytest -m api
```

```bash
pytest -m ui
```

### Просмотр Allure-отчёта локально

```bash
allure serve allure-results
```

---
</details>

<details>
<summary><strong>Запуск автотестов через Jenkins в Docker</strong></summary>

### Подготовка инфраструктуры

1. Клонировать репозиторий и перейти в директорию `docker`:

```bash
git clone https://github.com/dmitrii-peftiev/otus-qa-project-work.git
```

```bash
cd otus-qa-project-work/docker
```

2. Собрать образ и запустить контейнер:

```bash
docker compose up -d --build
```

3. Получить начальный пароль администратора Jenkins:

```bash
docker exec otus-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Первоначальная настройка Jenkins (http://localhost:8080/)

1. Ввести полученный пароль и установить рекомендуемые плагины (**Install suggested plugins**).
2. Установить плагин отчётов: **Manage Jenkins** → **Plugins** → **Available plugins** → **Allure Jenkins Plugin**.
3. Настроить утилиту Allure: **Manage Jenkins** → **Tools** → **Allure Commandline** → добавить инструмент с именем
   `allure` (оставить галочку **Install automatically**) → **Save**.
4. Создать задачу: **New Item** → ввести название → выбрать **Pipeline** → **OK**.
5. В разделе **Pipeline** выбрать **Pipeline script from SCM** → **Git**:
    * **Repository URL:** `https://github.com/dmitrii-peftiev/otus-qa-project-work.git`
    * **Branch Specifier:** `*/master`
    * **Script Path:** `Jenkinsfile`
6. Нажать **Save**.

### Запуск сборки и просмотр отчёта

1. Нажать **Build Now** (после первого запуска появится **Build with Parameters** для выбора `all`, `ui` или `api`).

2. После завершения сборки открыть отчёт по кнопке **Allure Report** в меню задачи.

### Управление и очистка Docker-ресурсов

* Остановка контейнера:

```bash
docker compose stop
```

* Полное удаление контейнера, томов и собранного образа:

```bash
docker compose down -v --rmi all
```

</details>
