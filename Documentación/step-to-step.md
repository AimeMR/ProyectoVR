# Plan de Proyecto: Sistema de Asistencia Hospitalaria con IA, AR y Robótica

Este documento detalla los pasos a seguir para el desarrollo de un sistema integral que combina Realidad Aumentada (AR), Inteligencia Artificial y Robótica para asistir en tareas hospitalarias, como la entrega de medicamentos.

---

## Componentes del Proyecto

* **Servidor Central (Laptop)**: Ejecutará el backend principal en C# (.NET Core) para la gestión de la comunicación y, posiblemente, se comunicará con un módulo de IA separado en Python. También alojará la base de datos.
* **Módulo de Inteligencia Artificial (IA)**: Un componente en Python (ejecutándose en la misma laptop o en un entorno separado) dedicado a los algoritmos de IA (YOLOv8, estimación de poses, etc.). Se comunicará con el Servidor Central (C#).
* **Aplicación Cliente (AR/Móvil)**: Desarrollada en Unity (C#) con Universal Render Pipeline (URP), inicialmente para teléfonos Android y luego extendida para gafas de Realidad Aumentada. Capturará vídeo, lo enviará al Servidor Central para procesamiento, y recibirá una imagen procesada (ej. con una ruta visualizada) para su renderización en AR.
* **Robot Autónomo** *(Actualmente no existente)*: Navegará por los pasillos del hospital siguiendo la ruta visualizada (en la aplicación AR o directamente si el robot tiene una interfaz AR/VR), identificará salas de pacientes y buscará una mesa específica para dejar medicamentos.

---

## Estructura del Repositorio GitHub

El proyecto se gestionará como un monorepo en GitHub, con una estructura clara para cada componente. La estructura de carpetas actual es ideal para esto:
/ARGUS-MedVision
├── Codigo/
│   ├── Cliente/          # Aplicación Cliente Unity (AR/Móvil)
│   │   ├── UnityAppAR_Phone/  # Proyecto Unity para teléfono/AR
│   │   │   ├── Assets/
│   │   │   ├── ProjectSettings/
│   │   │   ├── .gitignore     # Específico para este proyecto Unity
│   │   │   └── ...
│   │   └── UnityAppRobot_Client/ # Cliente Unity para el robot (si se usa Unity)
│   │       ├── Assets/
│   │       ├── ProjectSettings/
│   │       ├── .gitignore
│   │       └── ...
│   ├── Servidor/         # Servidor Central (C# .NET Core)
│   │   └── MiServidorWebSocket/
│   │       ├── MiServidorWebSocket.sln
│   │       ├── MiServidorWebSocket.csproj
│   │       ├── Program.cs
│   │       └── ...
│   ├── AI_Module/        # Módulo de Inteligencia Artificial (Python)
│   │   ├── src/
│   │   ├── requirements.txt
│   │   ├── venv/          # Ignorado por Git
│   │   ├── models/        # (Considerar Git LFS para modelos grandes)
│   │   ├── .gitignore     # Específico para Python
│   │   └── ...
│   ├── Robot/            # Código para el Robot Autónomo (C++/Python, si se desarrolla aquí)
│   │   └── ...
│   └── Pruebas/          # Pruebas integradas, utilidades, etc.
│       └── ...
├── Documentación/
├── .gitignore            # Global .gitignore para el monorepo
└── README.md

---

## Herramientas de Desarrollo

* **Servidor Central (C#):** Visual Studio Community
* **Módulo IA (Python):** Visual Studio Code
* **Aplicación Cliente (Unity C#):** Unity Editor (con Visual Studio Community como editor de scripts externo)
* **Control de Versiones:** Git y GitHub

---

## Fases y Pasos Detallados

### Fase 1: Conexión Cliente (AR/Móvil) al Servidor Central (WebSockets Bidireccional)

**Objetivo**: Establecer una comunicación en tiempo real y bidireccional entre la aplicación cliente Unity y el servidor central (C#).

#### 1.1 Configurar el Servidor WebSocket (C#)

* **Tecnología**: C# (.NET Core) con el middleware `System.Net.WebSockets`.
* **Herramienta**: Visual Studio Community.
* **Acción**: Desarrollar el `Program.cs` para escuchar conexiones WebSocket en el puerto `8080` (ej. `ws://localhost:8080/ws`).
    * Implementar un manejador de WebSocket (`HandleWebSocketConnection`) para recibir y enviar mensajes.
    * Gestionar conexiones activas (ej. con `ConcurrentBag<WebSocket>`) para posibles broadcasts.
* **Consideración**: Definir un protocolo de mensajes inicial simple (ej. strings) para pruebas, que luego evolucionará para frames de vídeo/datos procesados.

#### 1.2 Implementar el Cliente WebSocket en Unity (C#)

* **Tecnología**: C# con la librería `WebSocketSharp` (importada como `.dll` en `Assets/Plugins`).
* **Herramienta**: Unity Editor con Visual Studio Community.
* **Acción**: Crear el script `WebSocketClientManager.cs` en Unity.
    * Establecer conexión a `ws://[IP_Servidor]:8080/ws`.
    * Implementar métodos para enviar mensajes al servidor.
    * Implementar manejadores para `OnOpen`, `OnMessage`, `OnError`, `OnClose`.
    * **CRÍTICO**: Usar una cola (`mainThreadActions`) para procesar los callbacks de `WebSocketSharp` (que ocurren en hilos secundarios) en el hilo principal de Unity, evitando errores de acceso a la API de Unity.
    * Añadir lógica de reconexión automática si la conexión se pierde.
* **Configuración Unity Editor**: `Edit` > `Project Settings` > `Editor`: `Version Control Mode` a **"Visible Meta Files"** y `Asset Serialization Mode` a **"Force Text"**.
* **Pruebas**:
    * Ejecutar servidor C# (desde VS Community).
    * Ejecutar cliente Unity (en Unity Editor, modo Play).
    * Verificar mensajes en consolas de ambos (Unity Debug.Log y consola del servidor).

#### 1.3 Establecer Comunicación Bidireccional (Prueba Inicial)

* **App (Envío)**: El cliente Unity envía un mensaje de "hola" al conectarse y puede tener un botón para enviar mensajes de prueba.
* **Servidor (Recepción y Eco)**: El servidor recibe el mensaje y envía un mensaje de "eco" de vuelta al cliente.
* **App (Recepción)**: El cliente Unity recibe el mensaje de eco y lo muestra en la consola.

---

### Fase 2: Aplicación para la Captación y Envío de Imágenes (Teléfono/AR)

**Objetivo**: Capturar frames de vídeo desde la cámara del dispositivo móvil/AR y enviarlos eficientemente al servidor.

#### 2.1 Aplicación Cliente (AR/Móvil - Unity)

* **Acceso y Captura de Cámara**:
    * **Tecnología**: Unity con **AR Foundation** (para ARCore en Android y ARKit en iOS) para un acceso robusto y optimizado a los frames de la cámara AR.
    * **Acción**: Acceder a la cámara del teléfono o gafas AR y capturar frames.
    * **Consideración**: Optimizar resolución y FPS para balancear calidad visual y latencia/ancho de banda.
* **Envío de Imágenes al Servidor**:
    * **Acción**: Convertir los frames capturados a un formato de imagen comprimido (ej. JPEG, PNG en bytes) y enviarlos a través de la conexión WebSocket existente al servidor.
    * **Consideración**: Implementar streaming continuo o envío por lotes pequeños, dependiendo de la latencia requerida.
* **Recepción y Renderizado AR**:
    * **Acción**: Recibir la imagen procesada con la ruta del servidor.
    * **Tecnología (AR)**: **AR Foundation**.
    * **Acción**: Proyectar y renderizar la imagen recibida (con la ruta "pintada") en el entorno del mundo real a través de la cámara del dispositivo. Esto implicará mapeo de coordenadas 2D a 3D.
    * **Consideración**: Implementar calibración precisa del entorno físico y seguimiento robusto para una superposición AR efectiva.

#### 2.2 Aplicación para el Robot (Cliente Unity o Implementación Directa)

* **Definir Plataforma del Robot y SDK de Cámara**:
    * Decidir si el robot tendrá su propio cliente Unity (si tiene una pantalla y capacidad de cómputo) o si será una aplicación nativa en C++/Python.
    * **Tecnología**: Dependerá del hardware del robot (ej. ROS, OpenCV, APIs de cámara específicas del robot).
* **Implementar Captura y Envío**:
    * **Acción**: Capturar frames de vídeo desde la cámara del robot y enviarlos al Servidor Central.
    * **Alternativas de Conexión al Servidor Central**: Si el servidor ya tiene soporte WebSocket, podría ser WebSocket. Para alto rendimiento en C++ o Python, `gRPC` o incluso `RTSP` para video streaming puro son opciones viables para el envío de frames al módulo de IA.
    * **Consideración**: Conexión robusta y de baja latencia es esencial para la navegación autónoma.

---

### Fase 3: Procesamiento del Vídeo Recibido (Gafas/Teléfono)

**Objetivo**: Analizar el vídeo proveniente del cliente AR para detectar personas, estimar poses y posiblemente generar grafos de personas para reconocimiento o seguimiento.

#### 3.1 Comunicación Servidor C# <-> Módulo IA Python

* **Tecnología**: **gRPC** (recomendado para rendimiento y tipado fuerte entre C# y Python) o **WebSockets** (si la flexibilidad es prioritaria sobre el tipado RPC).
* **Acción**: Implementar un cliente gRPC/WebSocket en el servidor C# y un servidor gRPC/WebSocket en el módulo IA Python.
* **Protocolo**: Definir mensajes para enviar frames de vídeo (bytes) y recibir resultados de IA (JSON, Protobuf).

#### 3.2 Módulo de IA (Python)

* **Configurar YOLOv8**:
    * **Tecnología**: Python + PyTorch (o Ultralytics YOLOv8 library).
    * **Acción**: Instalar YOLOv8, cargar pesos pre-entrenados (ej. COCO para detección de personas).
* **Decodificar y Procesar Frames**:
    * **Acción**: Recibir los frames (bytes) del servidor C#, decodificarlos a un formato de imagen (ej. NumPy array) y procesarlos con OpenCV.
* **Detección de Personas**:
    * **Acción**: Utilizar YOLOv8 para detectar personas en los frames de vídeo.
* **Estimación de Poses**:
    * **Acción**: Integrar una librería de estimación de poses (ej. MediaPipe Pose, OpenPose) para obtener los keypoints de las personas detectadas.
* **Grafos de Personas (Definición y Comparación)**:
    * **Definir**: Aclarar qué representa un "grafo de persona" (ej. un esqueleto con conexiones y relaciones entre keypoints, o un grafo de interacción).
    * **Crear Referencias**: Desarrollar la lógica para grabar o extraer keypoints de poses de referencia y construir sus representaciones de grafos.
    * **Herramientas**: `NetworkX` para manipulación de grafos. Para comparación, métodos como distancias euclidianas entre keypoints o embeddings de grafos (GNNs si es avanzado).
    * **Objetivo**: Detectar patrones relevantes (ej. persona sentada, persona levantando el brazo, etc.) comparando los grafos en tiempo real con las referencias.
* **Generación de Imagen con Ruta**:
    * **Acción**: Basado en los resultados de la IA (detección, poses, comparación de grafos), generar una imagen con la ruta visualizada que el robot o el usuario de AR debe seguir. Esto implica dibujar líneas, flechas o superposiciones en la imagen original o una nueva.
* **Transmisión de Imagen al Servidor C#**:
    * **Acción**: Enviar la imagen procesada (como bytes JPEG/PNG) de vuelta al servidor C# a través de la comunicación gRPC/WebSocket.

---

### Fase 4: Procesamiento del Vídeo del Robot y Navegación

**Objetivo**: Identificar la "mesa objetivo" para la entrega de medicamentos y guiar al robot autónomo.

#### 4.1 Recepción del Vídeo (Módulo IA Python)

* **Acción**: Si el robot envía vídeo a la IA, decodificar los frames de la misma manera que en la Fase 3.

#### 4.2 Detección de Mesa con YOLOv8 (Módulo IA Python)

* **Problema**: La "mesa objetivo" no estará en los datasets pre-entrenados de YOLOv8 (ej. COCO).
* **Solución**: **Fine-tuning de YOLOv8**.
    1.  **Datos**: Crear un dataset de imágenes de la "mesa objetivo" en diferentes entornos hospitalarios, ángulos, iluminación.
    2.  **Anotación**: Usar herramientas como LabelImg o Roboflow para dibujar bounding boxes alrededor de las mesas en las imágenes.
    3.  **Entrenamiento**: Realizar un fine-tuning del modelo YOLOv8 pre-entrenado (ej. `yolov8n.pt`) utilizando tu dataset anotado.
    4.  **Acción**: Utilizar el modelo YOLOv8 personalizado para detectar la "mesa objetivo" en los frames de vídeo del robot.

#### 4.3 Lógica Adicional (Módulo IA Python)

* **Consideración**: Implementar lógica para inferir la ubicación de la mesa respecto al paciente, identificar características distintivas de la mesa o usar contexto adicional para confirmar la mesa correcta.

#### 4.4 Navegación del Robot y SLAM

* **Tecnología**: **ROS (Robot Operating System)** es el estándar de facto para la robótica. Librerías como `gmapping`, `cartographer` para SLAM (Simultaneous Localization and Mapping), y `move_base` para navegación autónoma.
* **Acción**:
    * **Mapeo**: Construir un mapa del entorno hospitalario (SLAM) utilizando los sensores del robot (LiDAR, cámaras de profundidad).
    * **Localización**: Localizarse en el mapa en tiempo real.
    * **Evasión de Obstáculos**: Navegar evitando obstáculos estáticos y dinámicos.
    * **Integración de Rutas**: Traducir la ruta generada por la IA (o directamente por el sistema de navegación) en waypoints o comandos de movimiento para el robot.
* **Comunicación con Robot**: Definir cómo el servidor (o el módulo de IA) enviará los comandos de navegación al robot (ej. ROS topics/services, API REST en el robot, etc.).

---

## Consideraciones sobre Tecnologías y Rendimiento

* **Servidor C# (.NET Core)**:
    * **Ventajas**: Excelente rendimiento, robustez, buen soporte para servicios web y gestión de concurrencia. Ideal para el "hub" central de comunicación.
    * **Desventajas**: No es el lenguaje nativo para IA.
* **Módulo IA (Python)**:
    * **Ventajas**: Ecosistema inigualable para IA (YOLOv8, PyTorch, OpenCV, MediaPipe), rápido desarrollo y prototipado.
    * **Desventajas**: Generalmente más lento que C++/C# para operaciones puramente computacionales (aunque las librerías de IA están altamente optimizadas).
* **Opciones de Comunicación (C# <-> Python)**:
    * **gRPC**: Preferible para RPC (Remote Procedure Calls) debido a su rendimiento, tipado fuerte y eficiencia en la serialización (Protobuf). Permite definir claramente los mensajes y servicios.
    * **WebSockets**: Si la comunicación es más un flujo de datos continuo sin llamadas a funciones remotas explícitas, también es una opción viable.
* **¿Es Python Suficiente para IA?**:
    * **Generalmente sí**, especialmente si se aprovechan las GPU. Las librerías de IA están altamente optimizadas. **Siempre se debe perfilar primero** para identificar cuellos de botella antes de considerar reescribir partes en C++/Cython.
* **C++ para el Robot**:
    * **Ventajas**: Control de bajo nivel, alta performance crítica para navegación y tiempo real.
    * **Desventajas**: Mayor complejidad de desarrollo.
    * **Opciones de Integración C++ con Python**: `PyBind11`, `Cython` si se necesita integrar código C++ de bajo nivel dentro de Python.

---

## Gestión de Datos

* **Base de Datos**: Seleccionar una base de datos relacional (PostgreSQL, MySQL) o NoSQL (MongoDB) según las necesidades de estructuración y escalabilidad de los datos (ej. logs, mapas SLAM, información de pacientes/mesas, auditoría).
* **Consideración de Rendimiento**: El cuello de botella en tiempo real suele estar en la red y el procesamiento de IA/visión, no en la latencia de la base de datos para operaciones no críticas.

---

## Consideraciones Adicionales y Futuras

* **Seguridad y Privacidad**:
    * **Comunicaciones**: Usar WebSockets Seguros (WSS) con TLS/SSL.
    * **Datos**: Cumplimiento con regulaciones como HIPAA (si aplica en el contexto hospitalario) y GDPR. Anonimización de imágenes y datos sensibles.
* **Latencia**: **CRÍTICA** para aplicaciones AR y control del robot. Optimizar la compresión de imágenes, la velocidad de procesamiento de IA y la eficiencia de la red.
* **Escalabilidad del Servidor**: Planificar la arquitectura para futuros aumentos de carga (ej. más clientes, más robots). Considerar principios de microservicios, balanceadores de carga si el servidor se distribuye.
* **Robustez y Manejo de Errores**: Implementar mecanismos de reconexión, reintentos y fallback en todas las capas (cliente, servidor, IA, robot).
* **Experiencia de Usuario (UX/UI)**: Para la aplicación AR, la visualización de la ruta debe ser intuitiva y clara. El robot debe tener indicadores de estado.
* **Navegación del Robot**: Considerar la evasión dinámica de obstáculos y la precisión en la entrega de medicamentos (ej. llegar al punto exacto de la mesa).
* **Base de Datos (detalles)**: Modelos de IA, mapas SLAM, logs de operaciones, historial de entregas, datos de pacientes (anonimizados).
* **Pruebas**:
    * **Unitarias**: Para cada componente (servidor C#, módulo IA, scripts Unity).
    * **Integración**: Probar la comunicación entre componentes (Cliente-Servidor, Servidor-IA).
    * **Entorno Real**: Pruebas exhaustivas en un entorno de hospital simulado.
* **Mantenimiento**: Planificar actualizaciones de modelos de IA, librerías y software.
* **Consumo Energético**: Optimizar el código y las operaciones para minimizar el consumo de batería en dispositivos móviles y el robot.
* **Condiciones Ambientales**: El entrenamiento de los modelos de IA debe incluir variaciones de iluminación, sombras, reflejos y posibles oclusiones en un entorno hospitalario.