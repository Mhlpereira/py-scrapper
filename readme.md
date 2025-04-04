Sistema utilizando o Makefile para automação 

```
Utilize o make all para executar os passos
```

Após a execução você pode usar o plsql para verificar as tabelas dentro do banco de dados no container docker

```
plsql PGPASSWORD=postgres psql -h localhost -U $(DB_USER)  -d $(DB_NAME)
```

Entrar no link para fazer as buscas

```
http://localhost:5173/
```