# Passos para rodar o docker no heroku

1 - acesse o diretório /docker_heroku e rode os comandos abixo

2 - heroku container:login

3 - heroku create

4 - heroku container:push web -a nome-do-app-que-o-heroku-gerou

5 - heroku container:release web -a nome-do-app-que-o-heroku-gerou

6 - heroku open -a nome-do-app-que-o-heroku-gerou

Este projeto está rondando em http://powerful-coast-79094.herokuapp.com/
