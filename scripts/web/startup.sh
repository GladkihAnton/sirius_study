#!/usr/bin/env bash


for argument in "$@"; do
  case $argument in
    -mm | --makemigrations)
      printf "Alembic make migrations"
      alembic -c conf/alembic.ini revision --autogenerate
      ;;

    -m | --migrate)
      printf "Alembic migration process...\n\n"
      alembic -c conf/alembic.ini upgrade head
      ;;

    -l | --loaddata)
      printf "Load data...\n\n"
      python ./utils/load_data.py fixtures/sirius.user.json
      ;;

    *)
      echo "Unknown argument"
      ;;
  esac
done


echo "Start service"
exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT
