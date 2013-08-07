#!/bin/bash

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_settings"

usage() {
    echo "USAGE: $0 [command]"
    echo "  test - run the django_email_changer tests"
    exit 1
}

case "$1" in
    "test" )
        django-admin.py test django_email_changer ;;
    * )
        usage ;;
esac