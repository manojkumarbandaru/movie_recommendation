# movie_recommendation

## Steps for Installtion

1. python3 -m venv env && source env/bin/activate
2. pip3 install --upgrade pip
3. pip install -r requirements.txt
4. docker-compose up -d
5. mysql -uroot -ppassword -P13310 -h 127.0.0.1 -e "CREATE DATABASE movie_recommendation"
6. python3 manage.py makemigrations
7. python3 manage.py migrate
8. python3 manage.py populate_database all

## To get the top n relevant movies list of a user
python3 manage.py recommend_movies.py <user_id> <top_n>