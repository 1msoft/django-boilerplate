#!/bin/sh

#deactivate first
if [ -n "$VIRTUAL_ENV" ] ; then
    deactivate
fi
# check project's virtual env
if [ -d "python_modules" ]; then
    # exist, so activate project's env
    source python_modules/bin/activate
else
    # create virtual env for this project.
    # python interpreter and all modules install to .python_modules
    virtualenv python_modules -p python2.7 --prompt=pyenv
    source python_modules/bin/activate
    if [ -n "$VIRTUAL_ENV" ]; then
        # install requirements
        pip install -r ./requirements.txt  \
            --extra-index-url  https://pypi.doubanio.com/simple/
        # code lint and format for ide
        pip install pylint pylint_django pep8 flake8 autopep8 mypy  \
            --extra-index-url  https://pypi.doubanio.com/simple/
        # not push to github
        echo "python_modules" >> .gitignore  
    fi
fi
export DEBUG='on'
# alias here
alias dj='python manage.py'
alias migrate='python manage.py migrate'
alias makemigrations='python manage.py makemigrations'
alias djshell='python manage.py shell'
