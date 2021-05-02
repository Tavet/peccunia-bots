# Peccunia Bots

## Local testing
- Agregar las credenciales restantes a default.env
- Construir el docker-compose
- Testear con el comando curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

## Twitter
AWS Lambda

PowerShell error: Set-ExecutionPolicy RemoteSigned

1. Crear ambiente virtual
python -m virtualenv .

2. Activar el ambiente
.\Scripts\activate.ps1

3. Ir a Libs -> site-package, instalar los requerimientos

cd .\Lib\site-packages
pip install -r requirements.txt
deactivate

4. Crear ZIP y subir al bucket de s3