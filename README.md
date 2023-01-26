# TreeMenu
![Django Support](https://img.shields.io/badge/django%20version-4.1.4-blue.svg)
## Requirements:
We need to make a django app that will implement a tree menu.

The following conditions must be met:
* Menu implemented via template tag
* Everything above the selected item is expanded. First nesting level
the selected item is also expanded.
* Stored in the database.
* Editable in the standard Django admin
* The active menu item is determined based on the URL of the current page
* There can be several menus on one page. They are identified by name.
* When you click on the menu, you go to the URL specified in it. URL can be
set both explicitly and via named url.
* to draw each
menu requires exactly 1 query to the database
  We need django-app, which allows you to add menus (one or more) to the database through
admin panel, and draw a menu by name on any desired page
  {% draw_menu &#39;main_menu&#39; %}
  When doing the job from libraries, you should only use Django and
the Python standard library.
this project is an implementation of a tree menu through django-tag

# description:
To solve this problem, I decided to add one field to the database,
which will contain the addresses of all the parents that need to be 
displayed for this element, maybe this is not the best solution, but
it really allows you to make only one request to the database for rendering

# Usage

```shell script
git clone https://github.com/Tyrannozavr/TreeMenu
```

```shell script
cd TreeMenu
```

```shell script
pip install -r requirements.txt
```
`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`

project have finished database with superuser by the address: http://127.0.0.1:8000/admin/
### login:dmiv
### password:123456

1. Create menu in admin panel. For example: name Menu
2. Create Items for menu, for example:
 * name 1, menu - Menu, parent - None
 * name 1.1 menu - Menu, parent - 1
3. then add {% load menu %} on you template
4. and add {% draw_menu 'Menu' %}

### you can go to http://127.0.0.1:8000/ to see the finished result
