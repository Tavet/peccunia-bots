# Peccunia Bots
Los bots están construidos sobre Docker para ser ejecutados, en su gran mayoría, en servicios Serverless (Lambda) de AWS.
Todas las llaves de acceso o tokens están encriptados bajo la llave de KMS [peccunia-env-key](https://us-west-2.console.aws.amazon.com/kms/home?region=us-west-2#/kms/keys/0cf05860-5660-421b-b2d6-9a9e24e437a4)

## Local Exectuion
- Agregar las credenciales restantes a default.env
- Construir el docker-compose
- Se puede hacer una petición http a la función.
```curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"type": "weekly","bucket":  "peccunia-assets","message": "test"}'```
