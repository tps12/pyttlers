find pyttlers/migrations/psql/*.sql | while read file ; do echo \\i $file | heroku pg:psql ; done

find pyttlers/migrations/mongo/*.js | while read file ; do mongo `heroku config:get MONGOHQ_URL | sed -e 's|mongodb://\(.*\):\(.*\)@\(.*\)|\3 -u \1 -p \2|'` $file ; done
