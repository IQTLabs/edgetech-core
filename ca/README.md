Please create a directory named "step", owned by the current user at the level where docker is run.

Prior to running please create the following files by running these commands:

echo -n mqtt | tee .mqtt_user
xkcdpass -d _ -n6 | tee .mqtt_password
xkcdpass -d _ -n6 | tee .ca_password


