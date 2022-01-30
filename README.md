# calorie_app

<Your Project Description>

## Repo Setup

### Prerequisites

* Python 3.9+
* Postgres 11+
* Redis 5

## Setup steps

1. Get the repo

    * Visit the repo and fork it
    * Clone the repo by using `git clone <repo/path>`
    * `cd calorie-app`

1. Set Environment Values

    * Copy the .env_template to .env
    * Fill the values of .env as required

1. Install requirements and pre-commit hooks

    1. Run the following command.

        make install

## Make

```
Usage: make <target>

Targets:
help           Show this help message
clean_pyc      Clean all *.pyc files
update         Update all necessary requirements and migrate
install        Install all necessary requirements
migrations     Make migrations
migrate        Apply migration files
test           Run tests
test-cov       Run tests with coverage
report         Coverage report
build          Build
pre_commit     Pre commit
collectstatic  Collects static files
server         Run python server only
admin          Creates Administrator account
version        Print version information
```

### Docker Setup and Run

`docker-compose up`

If you want fine tuned run, read next section

### Manual Setup and Run

1. Install virtualenv, pre-commit hook, requirements and migration.

    make install

1. To Runserver Locally (Not for Prod or staging):

    python manage.py runserver 8000

    Or

    make server

    The above command will run the server on port 8000

1. For Deployment purposes:

    Run: `make collectstatic`
    In the nginx/apache configuration, specify the path for static files to be served

1. To Run Celery on local

    `celery -A calorie_app.celery_app worker -B`


### Management Commands for translation

1. Find untranslated strings

    `python manage.py find_untranslated_strings`

    OR

    `make untranslated`

1. Copy output strings of above command and paste it in `calorie_app` sheet in
   respective language column `https://docs.google.com/spreadsheets/d/1ubfTgp6q74Juupq3ziemRI-9Htruu3eQCSkI8DGhVmc/edit#gid=275747298`

1. Download `calorie_app` sheet as csv file.

1. Copy translated strings back to django.po files.

    `python manage.py copy_translations --csv <path_to_downloaded_csv> --locale <locale>`


## Test Cases

    This ensure our code/functions is working as expected. Due to some changes/code update if a specific function breaks you will know about it.
    Structure:
    âââ app_name
        âââ tests
            âââ __init__.py
            âââ test_forms.py
            âââ test_models.py
            âââ test_views.py
    We have write test cases for each and every modules eg: models, forms, views etc. Add <test_> for each module name and place them in tests as above structure.

    Test module structure:
    <imports>

    <test class 1>
          def test_fun1:
                  .
                  .
                  .
          def test_funN:

    <test class 2>
            .
            .
            .
            .
    <test class n>

    Test class name should be <views/forms/utils name>Test.
    All the methods that are to be tested in our test classes should start with  <test_>
    Each test(method) should generally only test one scenario/flow of the function.
    Add a method <setUp> in each test class which will contain all setup code for test.
    For testing DRF classes follow: http://www.django-rest-framework.org/api-guide/testing/

    Test third party APIs: Functions which contain interaction with other external resource(api etc) use mock(http://www.voidspace.org.uk/python/mock/index.html).

    Run test cases:
    --------------

            1. All test cases at once:

                       make test

            2. Individual test case:

                    python manage.py test --settings=calorie_app.settings.test_settings \
                       apps.<app_name>.tests.<module_name>.<test_class>.<test_method>


                   apps.<app_name>.tests will run all test cases in this apps similarly
                   apps.<app_name>.tests.<module_name> in that module and
                   apps.<app_name>.tests.<module_name>.<test_class> in that class

## Test Coverage

    It keeps track of which lines of application code are executed, which ones are skipped (like comments), and which ones are never reached while executing test cases.

    Run coverage:
    -------------

        1.Run coverage on whole project/code base:
            make test-cov
        2.Run coverage on a particular app:
            coverage run --source=<module_path/app>[,<module_path/app>] manage.py test --settings=calorie_app.settings.test <module> [<module>]

    <module path/app>: apps.auth
    <module>: calorie_app.apps.auth

    Coverage report:
    ----------------
            make report
            option -m: Show line numbers of statements in each module that weren't executed

            OR

            coverage html
            It will generate `htmlcov` folder in project root. <project root>/htmlcov/index.html is index page for coverage listing


        The simplest reporting is textual summary:

        Name                                  Stmts   Miss Branch BrMiss  Cover   Missing
        ---------------------------------------------------------------------------------
        <module_1>                         103     53     51     33    44%   29, 47-48, 80-100, 104-111
        <module_2>                          74     23     14     10    63%   43-45, 57-72, 78-85
        ---------------------------------------------------------------------------------
        TOTAL                              177     76     65     43    51%

    Branch coverage:
         To measure branch coverage use --branch
         It will calculate no. of branches(if-else-if) have be covered by test case execution.
         http://nedbatchelder.com/code/coverage/branch.html#branch
