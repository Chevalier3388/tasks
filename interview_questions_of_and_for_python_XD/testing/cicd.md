## CI/CD
CI/CD (Continuous Integration / Continuous Delivery) — это практика автоматической сборки, 
тестирования и развертывания кода.

- ✅ Раннее обнаружение багов → тесты запускаются при каждом изменении кода.
- ✅ Ускорение feedback-цикла → разработчики сразу видят, что что-то сломалось.
- ✅ Стабильность продакшена → в прод попадает только проверенный код.

### Основные шаги:
1) Выбор CI/CD-инструмента (Jenkins, GitHub Actions, GitLab CI, CircleCI, etc.).
2) Конфигурация пайплайна (обычно через YAML-файл или Jenkinsfile).
3) Интеграция с репозиторием (запуск тестов при push / pull request).
4) Запуск тестов в изолированном окружении (Docker, виртуальные машины).
5) Обработка результатов (отчеты, уведомления в Slack/Email).

Примеры:

### GitHub Actions (для Python-проектов)
```yaml
name: Python CI

on: [push, pull_request]  # Запуск при пуше или PR

jobs:
  test:
    runs-on: ubuntu-latest  # Используем последний Ubuntu

    steps:
      # Шаг 1: Забираем код из репозитория
      - uses: actions/checkout@v4

      # Шаг 2: Устанавливаем Python
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      # Шаг 3: Устанавливаем зависимости
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt  # или pip install pytest, если без requirements.txt

      # Шаг 4: Запускаем тесты через pytest
      - name: Run tests
        run: |
          pytest tests/ --cov=./ --cov-report=xml  # с покрытием кода (если нужно)

      # Опционально: загружаем отчет о покрытии (например, в Codecov)
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        if: success()  # Только если тесты прошли
```
- Запускается при каждом push или pull request.
- Устанавливает Python 3.10.
- Ставит зависимости из requirements.txt.
- Запускает тесты через pytest (можно добавить --cov для покрытия).
- Отправляет отчет в Codecov (если подключен).

```yaml
name: Run Python Tests

on: [push]  # Запуск только при push (без PR)

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4  # Шаг 1: Получение кода
      
      - name: Install and test  # Шаг 2: Установка и тесты
        run: |
          python -m pip install pytest
          pytest tests/
```
1) Триггер: Запускается при каждом push в репозиторий.
2) Шаги:
- Забирает код (actions/checkout@v4)
- Устанавливает pytest и запускает тесты из папки tests/

### GitLab CI (для Python-проектов)
Файл: ```.gitlab-ci.yml```
```yaml
stages:
  - test  # Можно добавить другие этапы (deploy, lint и т.д.)

unit-tests:
  stage: test
  image: python:3.10  # Используем официальный образ Python
  before_script:
    - pip install --upgrade pip
    - pip install -r requirements.txt  # или pip install pytest
  script:
    - pytest tests/  # Простой запуск тестов
  artifacts:
    when: always  # Сохраняем отчеты даже при падении тестов
    paths:
      - test-reports/
    reports:
      junit: test-reports/junit.xml  # Для отображения в GitLab UI
```
- Запускает тесты в Docker-контейнере с Python 3.10.
- Устанавливает зависимости.
- Запускает pytest и сохраняет отчет в формате JUnit (для красивого отображения в GitLab).
- Артефакты (отчеты) сохраняются даже если тесты упали.


