## GUÍA DE INICIO RÁPIDO
Para lanzar el proyecto hay que haber cumplido con varios requisitos anteriores:
1. Descargar el proyecto.
2. Descomprimir la carpeta.
3. Mirar el siguiente punto llamado VARIABLES DE ENTORNO.
4. Descargar Docker Desktop.
5. Dejar Docker Desktop abierto.

Tras ello, nos vamos a la ruta en la que se encuentre el proyecto, exactamente a la misma altura que el archivo "docker-compose.yml"; debemos de ejecutar el comando docker-compose up --build -d, acceder al buscador y escribir el host que hayamos decidido ponerle.

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
El proyecto se ha diseñado en base a la Programación Orientada a Objetos.

1. Modelado de Datos:
   Se ha creado la clase Auditoría, que es la unidad central del proyecto; aplicando los siguientes conceptos de POO:
   - **Abstracción**: Se ha convertido un contrato legal en un objeto digital con atributos específicos como "puntos clave" o "banderas_rojas".
   - **Encapsulamiento**: El modelo gestiona sus propios datos y metadatos, asegurando la integridad de la información.
   - **Relación**: Se utiliza una relación de n:1 con la clase "User" de Django. Esto significa que varios contratos pueden pertenecer a un único usuario y que un usuario puede tener varios contratos.

2. Vista Basadas en Clases:
   Se han utilizado clases para gestionar la lógica de la interfaz:
   - **Herencia***: Clases como DashboardView y AuditoriaView heredan de la clase View de Django y de Mixins como LoginRequiredMixin. Esto permite reutilizar lógica de seguridad y comportamiento web sin duplicar código.
   - **Polimorfismo**: Se sobreescriben métodos estándar como get() y post() para adaptar el comportamiento de la clase a las necesidades específicas de la carga de archivos o la visualización del listado.

3. Lógica de Negocio y Modularidad:
   - **Interoperabilidad entre Objetos**: El sistema trata los archivos PDF como objetos de flujo de datos que se pasan entre servicios. La lógica de procesamiento en "EnviarPDF" actúa como un mediador que transforma la respuesta cruda de la IA en una instancia persistente del objeto "Auditoria".
   - **Gestión de Estados**: El objeto "Auditoria" es capaz de almacenar resultados complejos mediante campos JSON, lo que permite que cada instancia mantenga el contexto completo de su análisis de forma independiente.
