# UOH Survivors

Videojuego simple basado en "Vampire Survivors", un roguelike de disparos por oleadas, donde el objetivo es sobrevivir la mayor cantidad de tiempo posible. El juego tiene la temática de la UOH y solo incluirá una parte de las mecánicas y jugabilidad del juego original.

### Requerimientos

Para desarrollar y ejecutar el juego se requiere de:

- Python 3.12.x
- Pygame 2.6.x

### Instalación

Una vez teniendo Python 3.12, se recomienda usar un entorno virtual para instalar las librerias, el cual se puede crear de la siguiente manera:

- python3.12 -m venv uoh-survivors

Una vez creado el entorno, se activa con el siguiente comando, dependiendo si se está en Windows o Mac/Linux:

- Windows: uoh-survivors\Scripts\activate

- Mac/Linux: source uoh-survivors/bin/activate

Finalmente, para instalar la libreria necesaria, se utiliza:

- pip install pygame

Con esto, se tendrá el entorno listo para jugar y desarrollar el juego

### Ejecución del juego y cómo jugar

Para abrir el juego, se debe ejecutar el archivo main.py, de la siguiente manera:

- python main.py

Esto abrirá la ventana del juego, iniciando en el menú principal. Los controles básicos del juego son:

- WASD para mover al personaje
- 123 para seleccionar la mejora del personaje al subir de nivel
- Esc para abrir el menú de pausa

### Armas

Además del proyectil básico y del orbe giratorio, el juego cuenta con el **RAM Boomerang**, un arma que se obtiene recogiendo un ítem rectangular de color verde que los enemigos sueltan al morir (10% de probabilidad).

- Cada vez que se recoge un ítem de RAM Boomerang, el arma sube de nivel y aumenta su daño.
- El boomerang se lanza automáticamente hacia el enemigo más cercano, viaja en línea recta hasta una distancia máxima y luego regresa hacia el jugador, dañando enemigos tanto en la ida como en la vuelta.
- Al alcanzar el nivel 3, el arma evoluciona a **Segmentation Fault**: cada cierto tiempo la pantalla simula un error de segmentación (overlay con mensajes tipo `SIGSEGV`, `core dumped`, entre otros) que inflige daño masivo a todos los enemigos visibles en pantalla.

A diferencia del daño, la velocidad de ataque y la velocidad de movimiento (que se eligen manualmente al subir de nivel), el RAM Boomerang sube de nivel solo al recolectar su ítem correspondiente en el mapa, sin ocupar un espacio en el menú de mejoras.

### Estado del juego

El juego UOH Survivors es totalmente jugable, sin embagro, aun queda mucho desarrollo por delante, y muchas implementaciones que hacer para mejorar la jugabilidad y el diseño gráfico del juego.

### Futuras implementaciones

Algunas de las implementaciones a realizar en el futuro son:

- Agregar sprites al mapa y enemigos.
- Agregar nuevos items que ayuden al jugador, como por ejemplo, kits curativos que curen al jugador, amuletos que aumenten la vida maxima, items de invulnerabilidad temporal, entre otros.
- Agregar nuevas armas con distintos daños y areas de efecto, como escopetas que disparen varias balas a la vez, armas cuerpo a cuerpo, cañones laser que hagan daño constante, entre otros. (Ya se agregó una primera arma adicional: el RAM Boomerang, con su evolución Segmentation Fault).
- Agregar música al gameplay.
- Mejorar interfaz gráfica del menú principal y del gameplay.
- Agregar más skins.
- Agregar nuevos tipos de enemigos.
- Agregas bosses y peleas contra bosses que otorguen recompensas al jugador.

Se continuará trabajando para implementar todas estas funcionalidades y más.

### Créditos

Autor: Felipe Scanda