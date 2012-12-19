find pyttlers/migrations/psql/*.sql | while read file ; do psql -X -d pyttlers_$1 -f $file ; done

find pyttlers/migrations/mongo/*.js | while read file ; do mongo pyttlers_$1 $file ; done
