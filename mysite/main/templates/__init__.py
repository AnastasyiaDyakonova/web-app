"""В данной директории хранятся поддиректория main, содержащая шаблоны страниц,
отображаемые при переходе по определенному адресу из представлений.

1. success.html - страница, вызываемая в случае успеха при добавлении записей в базу данных;

2. forms.html - базовый шаблон, от которого наследуются шаблоны:

 create.html - страница с формой для заполнения отчета водителя;

 route.html - страница с формой для заполнения справочника маршрутов;

 step.html - страница с формой для заполнения водителем шагов маршрута;

 task.html - страница с формой для заполнения заданий от менеджера;

3. select_catalog_driver.html - страница, содержащая таблицу с данными водителей, сформированными на основании данных из источников;

4. select_driver_task_url.html - страница, содержащая таблицу с невыполненными заданиями для водителей;

5. select_report.html - страница, содержащая таблицу с последними 10 отчетами, сформированными на основании данных из источников;

6. select_url_route.html - страница, содержащая таблицу с номерами и ссылками на маршруты, сформированными на основании данных из источников;

7. select_dwh_report.html - страница, содержащая кнопку для скачивания отчета и таблицу с отчетами, сформированными на основании данных из хранилища;

8. select_itog_report.html - страница, содержащая кнопку для скачивания отчета и таблицу с общим отчетом за прошлый месяц, сформированными на основании данных из хранилища.

"""