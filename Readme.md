### Configuración Environment
- Recordar setear el _venv_ con pycharm o vía consola.
`ctrl+alt+s` -> project->Python Interpreter -> Add Interpreter -> Add Local Interpreter -> (seleccionar uno que exista o crear un nuevo)

- Creando un nuevo _venv_ consola: `python3.** -m venv my-venv`

### Instalación
- Instalar dependencias: `pip install -r requirements.txt`
- Chequear que se haya instalado bien: `pip freeze` `pip list` 
- aws cli: `pip install awscli`(omitir si ya está instalado globalmente)

### aws cli
- `aws configure --profile jorge-admin` (jorge-admin: profile con permiso de admin) 
- `export AWS_PROFILE=jorge-admin`
- `aws s3 ls` (chequea todos los buquets, el profile configurado ahora es jorge-admin, no es necesario --profile=jorge-admin)
- `aws s3 mb s3://master-lambda-gharchive` (crear/make bucket)
- `aws s3 ls s3://master-lambda-gharchive` (chequea el contenido del bucket)
- `aws s3 rb s3://master-lambda-gharchive` (remove bucket)

### env vars
- recordar activar en el config del main y en la consola de python las variables de entorno que se vayan a usar(alt+ctrl+s) como AWS_PROFILE
