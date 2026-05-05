## GUÍA DE INICIO RÁPIDO
Para lanzar el proyecto hay que haber cumplido con varios requisitos anteriores:
1. Descargar el proyecto.
2. Descomprimir la carpeta.
3. Mirar el siguiente punto llamado VARIABLES DE ENTORNO.
4. Descargar Docker Desktop.
5. Dejar Docker Desktop abierto.

Tras ello, nos vamos a la ruta en la que se encuentre el proyecto, exactamente a la misma altura que el archivo Dockerfile; y debemos de ejecutar el comando docker-compose up --build.

## VARIABLES DE ENTORNO
Para poder lanzar correctamente el proyecto, necesitamos unas variables de entorno para gestionar credenciales y configuraciones críticas:
1. Localiza el archivo ".env.example" en la raíz del proyecto.
2. Crea una copia de dicho archivo con el nombre ".env".
3. Configura las siguientes variables:
   - **DB_...**: Credenciales para la conexión a la Base de Datos PostgreSQL.
   - **GOOGLE_API_KEY**: Clave API obtenida en Google AI Studio.
   - **MAX_TOKENS**: Límite de tokens para las respuestas de la IA.
   - **SECRET_KEY**:  Clave secreta para Django.
   - **ALLOWED_HOSTS**: Lista de dominios o IPs permitidas separadas por comas (ejemplo: localhost, ).

## ESQUEMA DE CLASES
