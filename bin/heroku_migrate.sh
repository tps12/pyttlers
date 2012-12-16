find pyttlers/migrations/psql/*.sql | while read file ; do echo \\i $file | heroku pg:psql ; done
