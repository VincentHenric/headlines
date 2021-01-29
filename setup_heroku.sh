#!/bin/bash
read -p 'Enter the name of the app on heroku: ' name

heroku login

name_prod="$name-prod"
name_dev="$name-dev"

heroku create $name_prod
heroku create $name_dev

git remote add prod git@heroku.com:$name_prod.git
git remote add dev git@heroku.com:$name_dev.git

git push dev master
git push prod master

echo environment $name_prod has been created
echo environment $name_dev has been created
