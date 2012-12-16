find pyttlers/migrations/psql/*.sql | while read file ; do psql -X -d pyttlers_$1 -f $file ; done
