# Api de prueba

##### Esta api esta hecha en base a test de selección solicitado para la empresa a la cual esta dirigida

Variables de entorno se encuentran en el archivo "Dockerfile" en la carpeta raiz en caso de querer ser modificados

Para poder ejecutar la aplicación, usar los siguientes comandos en la carpeta de la API:

```sh
$ docker build . --tag NOMBRE_DE_IMAGEN
$ docker run -p PUERTO_A_EXPONER:5000 [-d] NOMBRE_DE_IMAGEN
```

En donde NOMBRE_DE_IMAGEN es el nombre que se le dara a la imagen para ser ejecutada y PUERTO_A_EXPONER es el puerto al cual se podra acceder a la aplicacion desde el navegador o la herramienta que sea ocupada para acceder a la API.
