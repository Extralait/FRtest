# FRtest

### Project run
```vim
docker build -t web-image ./back
docker-compose up -d
docker-compose exec web python manage.py create_admin
docker-compose exec web python manage.py collectstatic
```

### Базовый URL

***http://localhost/api/v1***

### Модель пользователя
***http://localhost/api/v1/users/*** \
Доступна регистрация и авторизация, также доступны вложенные URL \
***/users/{id}*** \
***/users/{id}/created-quiz*** \
***/users/{id}/created-quiz/{id}*** \
***/users/{id}/created-quiz/{id}/questions*** \
***/users/{id}/created-quiz/{id}/questions/{id}*** \
***/users/{id}/created-quiz/{id}/questions/{id}/choices*** \
***/users/{id}/created-quiz/{id}/questions/{id}/choices/{id}*** \
***/users/{id}/passed-quiz*** \
***/users/{id}/passed-quiz/{id}*** \
***/users/{id}/passed-quiz/{id}/answers*** \
***/users/{id}/passed-quiz/{id}/answers/{id}*** \
Все модели доступны для редактирования, удаления и т.д. \
Для модели теста также есть экстра действие для редактирования текущего пользователя \
***http://localhost/api/v1/users/me***




### Модель теста
***http://localhost/api/v1/quiz/*** \
Также доступны вложенные URL
***/quiz/{id}*** \
***/quiz/{id}/questions*** \
***/quiz/{id}/questions{id}*** \
***/quiz/{id}/questions{id}/choices*** \
***/quiz/{id}/questions{id}/choices{id}*** 

Создать тест можно с помощью вложенного сериализатора \
на запись, вот пример json для POST запроса
```json
{
    "name": "First",
    "is_active": true,
    "start_date": "2022-01-11T00:24:00+03:00",
    "end_date": "2022-01-29T00:24:00+03:00",
    "questions": [
        {
            "question_text": "first",
            "question_type": "text",
            "is_required": false
        },
        {
            "question_text": "first",
            "question_type": "text",
            "is_required": false
        },
        {
            "question_text": "first",
            "question_type": "text",
            "is_required": false
        },
        {
            "question_text": "first",
            "question_type": "checkbox",
            "is_required": false,
            "choices": [
                {
                    "title": "Первый"
                },
                {
                    "title": "Второй"
                },
                {
                    "title": "Третий"
                },
                {
                    "title": "Четвертый"
                }
            ]
        },
        {
            "question_text": "first",
            "question_type": "radio",
            "is_required": false,
            "choices": [
                {
                    "title": "Первый"
                },
                {
                    "title": "Второй"
                },
                {
                    "title": "Третий"
                },
                {
                    "title": "Четвертый"
                }
            ]
        }
    ]
}
```
Далее детали этого теста уже в api
```json
{
    "id": 1,
    "name": "first",
    "owner": 1,
    "is_active": true,
    "start_date": "2022-01-11T00:24:00+03:00",
    "end_date": "2022-01-29T00:24:00+03:00",
    "questions": [
        {
            "id": 1,
            "question_text": "First",
            "question_type": "text",
            "is_required": false,
            "choices": []
        },
        {
            "id": 2,
            "question_text": "First",
            "question_type": "text",
            "is_required": false,
            "choices": []
        },
        {
            "id": 3,
            "question_text": "First",
            "question_type": "text",
            "is_required": false,
            "choices": []
        },
        {
            "id": 4,
            "question_text": "First",
            "question_type": "checkbox",
            "is_required": false,
            "choices": [
                {
                    "id": 1,
                    "title": "Первый"
                },
                {
                    "id": 2,
                    "title": "Второй"
                },
                {
                    "id": 3,
                    "title": "Третий"
                },
                {
                    "id": 4,
                    "title": "Четвертый"
                }
            ]
        },
        {
            "id": 5,
            "question_text": "First",
            "question_type": "radio",
            "is_required": false,
            "choices": [
                {
                    "id": 5,
                    "title": "Первый"
                },
                {
                    "id": 6,
                    "title": "Второй"
                },
                {
                    "id": 7,
                    "title": "Третий"
                },
                {
                    "id": 8,
                    "title": "Четвертый"
                }
            ]
        }
    ]
}
```

Для модели теста также есть экстра действие для ответа на тест \
***http://localhost/api/v1/quiz/1/answer/***
Пример ответа конкретно на этот тест (Цифры в ответах - id choice, ключи - id question)
```json
{
  "1": "Any text answer",
  "2": "Any text answer",
  "3": "Any text answer",
  "4": [
    1,
    2,
    3
  ],
  "5": 8
}
```

Admin-панель могу доделать, если нужно