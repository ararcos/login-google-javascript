#! /bin/bash
SERVICE=$1
BODY=$2

if [ -z "$SERVICE" ] ; then
    echo "Service shouldn't be empty"
    exit 1
fi

case "$SERVICE" in
    get)
        PORT="9000"
        ;;
    update)
        PORT="9001"
        ;;
    find)
        PORT="9002"
        ;;
    delete)
        PORT="9003"
        ;;
    create)
        PORT="9004"
        ;;
    *)
        echo "$SERVICE is not supported. Use [get, update, find, delete, create]"
        exit 2
        ;;
esac

if [ -z "$BODY" ] ; then
    echo "Body shouldn't be empty"
    exit 3
fi

curl -XPOST "http://localhost:$PORT/2015-03-31/functions/function/invocations" -d "$BODY"
