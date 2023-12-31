# Проект для отборочного этапа конкурса Иорин Богданов (РТУ МИРЭА)

![Изображение](/assets/front.png)

## Особенности

- Запись изменений в таблицу с использованием метода `/update`
- Вывод данных из главной таблицы с использованием `/main`
- Загрузка главной таблицы с помощью `/main_download`
- Список доступных файлов с использованием `/list_files`
- Загрузка определенного файла из списка с помощью `/get_current_files/{item_str}`
- Аналитика 2-ой части: Разбивка выполнения операций по плану и факту по участкам в виде таблицы и графика с использованием `/analytics`
- Фильтрация по фамилии в аналитике 2-ой части с помощью `/filter_analytics/{surname}`

![Изображение Swagger](/assets/swagger.png)

## Документация

Изучите документацию API с помощью Swagger UI:

[Документация API Swagger](https://{url}/docs#/)

## Стек технологий

- Бэкэнд: FastAPI
- Фронтенд: React
- Документация API Swagger: [Swagger UI](https://{url}/docs#/)
