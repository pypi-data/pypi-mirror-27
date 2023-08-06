
BasiliskJS - Scriptable Headless WebKit
=========================

`BasiliskJS <https://pypi.python.org/pypi/BasiliskJS>`_ Представляет собой безглавую версию `PhantomJS <http://phantomjs.org>`_ с JavaScript.

Возможность
============

- **Быстрое тестирование**. Возможность быстрого тестирования без браузера!
- **Автоматизация dom**. Простой интерфейс.
- **Работа с js**. Есть возможность запускать JavaScript.
- **Захват экрана**. Возможность сделать снимок страницы любого размера.

Пример работы
-------------
Простой запрос на http://phantomjs.org/.

.. code-block:: python

    >>> from basilisk import PhantomJS
    >>> PhantomJS.get('http://phantomjs.org/')

Запрос с выполнением js.

.. code-block:: python

    from basilisk import PhantomJS
    url = 'http://phantomjs.org/documentation/'
    js_ex = """
    var temp = {};
    for (var i = 0; i != document.getElementsByClassName('nav-item-name').length; i++) {
       temp[i] = document.getElementsByClassName('nav-item-name')[i].innerText;
     }
       return temp;
    """
    print(PhantomJS.get(url=url, screenshot=True, load_image=True, js_evalute=js_ex ))

    #Результат
     {'status': 'success',
     'js': {'24': 'Release Preparation',
      '25': 'Crash Reporting', '26': 'Bug Reporting',
      '20': 'Related Projects', '21': 'Contributing',
      '22': 'Source Code', '23': 'Test Suite',
      '1': 'Build', '0': 'Download', '3': 'Release Names',
      '2': 'Releases', '5': 'Quick Start', '4': 'REPL',
      '7': 'Screen Capture', '6': 'Headless Testing',
      '9': 'Page Automation', '8': 'Network Monitoring',
      '11': 'Command Line Interface', '10': 'Inter Process Communication',
      '13': 'FAQ', '12': 'Troubleshooting', '15': 'Best Practices',
      '14': 'Examples', '17': 'Supported Web Standards',
      '16': 'Tips and Tricks',
      '19': "Who's using PhantomJS?", '18': 'Buzz'}}


Простой запрос с простым выполнением js

.. code-block:: python

    from basilisk import PhantomJS

    js = [
        "document.getElementsByClassName('explanation')[0].innerText"
        ]

    PhantomJS.get('http://phantomjs.org/', js = js)



Показать html контент

.. code-block:: python

    >>> from basilisk import PhantomJS
    >>> PhantomJS.get('http://phantomjs.org/', content=True)



Параметры метода get()
-------------    
- **url**. - url для get запроса.
- **content**. - Паказать content, по умолчанию( False ).
- **load_image**. - Загрузка изаброжений сайта, по умолчанию( False ).
- **userAgent**. - User-Agent, по умолчанию( "BasiliskJS" ).
- **js_evalute**. - Выполнить полноценый js.
- **get_url**. - Показать url, по умолчанию( False ).
- **js**. - Скрипты js для работы с DOM.
- **screenshot**. - Сделать скриншот сайта, по умолчанию( False ).
- **image_name**. - Название файла скриншот или полный путь к файлу , по умолчанию( BasiliskJS ).
- **exit**. - Закрытие браузера, по умолчанию( True ).
- **command**. - Для работы требуется браузер PhantomJS, параметр отвечает за путь к нему, по умолчанию( phantomjs ).

Развитие
-------------   
На данный момент мы на стадии Pre-Alpha. Вы можете увидеть сообщения об ошибках и т.д. 
    