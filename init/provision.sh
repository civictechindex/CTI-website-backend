echo ***PERFORMING DATABASE MIGRATIONS***
python /code/manage.py migrate
echo ***PROVISIONING DEFAULT USER***
cat /code/init/default_user.py | python /code/manage.py shell
echo ***LOADING INITIAL DATASET***
# TODO: This belongs in a migration.
python /code/manage.py import_initial_data /code/init/data.csv 
