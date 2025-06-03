# Plan de Proyecto: Sistema de Asistencia Hospitalaria con IA, VR y Robótica

Este documento detalla los pasos a seguir para el desarrollo de un sistema integral que combina Realidad Virtual/Aumentada, Inteligencia Artificial y Robótica para asistir en tareas hospitalarias, como la entrega de medicamentos.

---

## Componentes del Proyecto

- **Servidor Central**: Un laptop (actualmente) que ejecuta algoritmos de IA y aloja la base de datos.
- **Aplicación Cliente (VR/Móvil)**: Desarrollada en Unity, inicialmente para teléfonos Android y luego para gafas VR. Captura vídeo, lo envía al servidor para procesamiento, y recibe una imagen con una ruta que se "pinta" en el suelo.
- **Robot Autónomo** *(Actualmente no existente)*: Navegará por los pasillos del hospital siguiendo la ruta visualizada, identificará salas de pacientes y buscará una mesa específica para dejar medicamentos. Esto implicará entrenar un modelo para reconocer dicha mesa.

---

## Fases y Pasos Detallados

### Fase 1: Conexión Gafas/Teléfono al Servidor (Transmisión Bicanal con WebSockets)

**Objetivo**: Establecer una comunicación en tiempo real y bidireccional entre la aplicación cliente y el servidor.

#### Configurar el Servidor WebSocket

- **Tecnología**: Python (librerías como `websockets` o `FastAPI` con soporte WebSocket).
- **Acción**: Desarrollar un script que escuche conexiones WebSocket en un puerto específico.
- **Consideración**: Definir protocolo de mensajes claro (frames de vídeo, datos procesados).

#### Implementar el Cliente WebSocket en Unity

- **Tecnología**: C# (nativo de Unity o librerías como `NativeWebSocket`).
- **Acción**: Código en Unity para conexión, envío y recepción de mensajes.
- **Consideración VR**: Minimizar latencia.

#### Establecer Comunicación Bidireccional

- **App (Envío)**: Capturar y enviar frames.
- **Servidor (Proceso)**: Procesar con IA.
- **Servidor (Envío)**: Enviar imagen con ruta.
- **App (Recepción)**: Renderizar imagen procesada.
- **Optimización**: Comprimir imágenes (ej. JPEG).

---

### Fase 2: Aplicación para la Captación y Envío de Imágenes

#### 2.1 Aplicación para Teléfono/Gafas VR (Unity)

**Acceso y Captura de Cámara**

- **Tecnología**: Unity (`WebCamTexture`).
- **Acción**: Acceder a cámara Android, capturar frames.
- **Consideración**: Optimizar resolución/FPS.

**Envío de Imágenes al Servidor**

- **Acción**: Enviar frames vía WebSocket (posiblemente comprimidos).
- **Consideración**: Streaming o lotes pequeños.

**Recepción y Renderizado AR**

- **Acción**: Recibir imagen con ruta.
- **Tecnología (AR)**: ARCore + AR Foundation.
- **Consideración**: Calibración precisa en entorno físico.

#### 2.2 Aplicación para el Robot

**Definir Plataforma del Robot y SDK de Cámara**

- **Tecnología**: Probable uso de C++ o Python, con ROS/OpenCV/etc.

**Implementar Captura y Envío**

- **Acción**: Capturar frames y enviarlos.
- **Alternativas a WebSockets**: gRPC o RTSP.
- **Consideración**: Conexión robusta esencial.

---

### Fase 3: Procesamiento del Vídeo Recibido (Gafas/Teléfono)

**Objetivo**: Analizar el vídeo para detectar personas y entender el entorno.

#### Configurar YOLOv8

- **Tecnología**: Python + PyTorch.
- **Acción**: Instalar YOLOv8, cargar pesos (COCO).

#### Decodificar y Procesar Frames

- **Acción**: Decodificar a NumPy array, procesar con OpenCV.

#### Detección de Personas

- **Acción**: Detectar personas con YOLOv8.

#### Estimación de Poses

- **Acción**: Usar MediaPipe/OpenPose para keypoints.

#### Grafos de Personas

- **Definir**: ¿Qué es un grafo de persona?
- **Crear Referencias**: Grabar, extraer keypoints, construir grafos.
- **Herramientas**: `NetworkX`, GNNs (opcional).

#### Comparación de Grafos en Tiempo Real

- **Acción**: Construir y comparar con referencias.
- **Métodos**: Distancias euclidianas, isomorfismo, embeddings.
- **Objetivo**: Detectar patrones relevantes.

#### Enviar Imagen con Ruta

- **Acción**: Dibujar ruta basada en resultado de comparación.
- **Transmisión**: Enviar imagen procesada al cliente.

---

### Fase 4: Procesamiento del Vídeo del Robot

**Objetivo**: Identificar la "mesa objetivo" para entrega de medicamentos.

#### Recepción del Vídeo

- **Acción**: Decodificar como en fase 3.

#### Detección de Mesa con YOLOv8

- **Problema**: No está en dataset base.
- **Solución**: Fine-tuning.

**Pasos para Fine-tuning**:

1. **Datos**: Crear dataset con mesa objetivo.
2. **Anotación**: Bounding boxes con LabelImg/Roboflow.
3. **Entrenamiento**: Con pesos base de COCO.
4. **Acción**: Detectar mesa con el modelo personalizado.

#### Lógica Adicional

- **Consideración**: Ubicación respecto al paciente, características, contexto.

#### Navegación del Robot y SLAM

- **Tecnología**: ROS (`gmapping`, `cartographer`, `move_base`).
- **Acción**: Construir mapa, localizarse, evitar obstáculos.
- **Integración**: Traducir ruta en waypoints.

---

## Consideraciones sobre Tecnologías

### Python para IA

- **Ventajas**: Ecosistema amplio, fácil de prototipar.
- **Estándar**: Para IA (YOLOv8, PyTorch, OpenCV).

### C++ para Gestión de Datos/Rendimiento

- **Ventajas**: Alta performance.
- **Desventajas**: Mayor complejidad.

### Opciones de Integración

- `Cython`, `PyBind11`: Extensiones Python en C++.
- `gRPC`, IPC: Comunicación entre Python y C++.
- APIs C++: OpenCV, TensorFlow Lite, ONNX Runtime.

### ¿Es Python Suficiente?

- **Generalmente sí**, especialmente con GPU. Perfilar primero.

---

## Gestión de Datos

- **Base de Datos**: PostgreSQL, MySQL, MongoDB.
- **Tiempo real**: Bottleneck suele estar en red/IA, no en memoria.

---

## Consideraciones Adicionales

- **Seguridad y Privacidad**:
  - WSS, TLS/SSL.
  - Cumplimiento con HIPAA/GDPR.
  - Anonimización de imágenes.

- **Latencia**: Crítica para VR y control del robot.

- **Escalabilidad del Servidor**:
  - Microservicios.
  - Balanceadores de carga.

- **Robustez y Errores**:
  - Reconexión, reintentos, fallback.

- **UX/UI**:
  - Intuitiva, clara visualización.
  - Indicadores de estado en robot.

- **Navegación**:
  - Evasión dinámica de obstáculos.
  - Precisión en entrega.

- **Base de Datos**:
  - Modelos, mapas SLAM, logs, auditoría.

- **Pruebas**:
  - Unitarias, integración, entorno real.

- **Mantenimiento**:
  - Actualizaciones planificadas.

- **Consumo Energético**:
  - Duración batería en móviles y robot.

- **Condiciones Ambientales**:
  - Entrenamiento debe incluir variaciones (iluminación, reflejos).

---

