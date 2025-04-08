# Biblioteca de YOLO8 y comandos útiles

YOLO8 (también conocido como YOLOv8) es la versión mejorada del popular modelo de detección de objetos YOLO (You Only Look Once) desarrollado por Ultralytics. Te mostraré los principales componentes de la biblioteca y comandos útiles.

## Instalación de YOLO8

```python
# Instalación desde pip
pip install ultralytics

# Alternativamente, desde GitHub
pip install git+https://github.com/ultralytics/ultralytics.git
```

## Estructura principal de YOLO8

YOLOv8 tiene varios modos principales:

1. **Detección (Detection)** - Detecta objetos en imágenes y vídeos
2. **Segmentación (Segmentation)** - Segmenta objetos a nivel de píxel
3. **Clasificación (Classification)** - Clasifica imágenes en categorías
4. **Estimación de poses (Pose)** - Detecta puntos clave del cuerpo humano

## Comandos básicos de YOLO8

### Importar la biblioteca

```python
from ultralytics import YOLO
```

### Cargar un modelo preentrenado

```python
# Cargar modelo de detección
model = YOLO('yolov8n.pt')  # modelo nano
# También disponibles: yolov8s.pt (small), yolov8m.pt (medium), yolov8l.pt (large), yolov8x.pt (xlarge)

# Cargar modelo de segmentación
seg_model = YOLO('yolov8n-seg.pt')

# Cargar modelo de clasificación
cls_model = YOLO('yolov8n-cls.pt')

# Cargar modelo de pose
pose_model = YOLO('yolov8n-pose.pt')
```

### Inferencia (predicción)

```python
# Inferencia en imagen
results = model('ruta/a/imagen.jpg')

# Inferencia en video
results = model('ruta/a/video.mp4')

# Inferencia con webcam
results = model(0)  # 0 para la webcam predeterminada
```

### Procesamiento de resultados

```python
# Mostrar resultados
for r in results:
    print(r.boxes)  # Boxes object for bounding boxes outputs
    print(r.masks)  # Masks object for segmentation masks outputs
    print(r.probs)  # Class probabilities for classification outputs
    print(r.keypoints)  # Keypoints object for pose outputs
```

### Visualización de resultados

```python
# Visualizar resultados
results = model('imagen.jpg')
res_plotted = results[0].plot()
import cv2
cv2.imshow("Resultados", res_plotted)
cv2.waitKey(0)
```

## Entrenamiento

```python
# Entrenar un modelo de detección con parámetros personalizados
model.train(data='ruta/a/data.yaml', epochs=100, imgsz=640)

# Entrenar para segmentación
seg_model.train(data='ruta/a/seg_data.yaml', epochs=100, imgsz=640)

# Entrenar para clasificación
cls_model.train(data='ruta/a/cls_data.yaml', epochs=100, imgsz=224)

# Entrenar para pose
pose_model.train(data='ruta/a/pose_data.yaml', epochs=100, imgsz=640)
```

## Validación

```python
# Validar modelo
metrics = model.val()
```

## Exportar modelos

```python
# Exportar a diferentes formatos
model.export(format='onnx')  # Exportar a ONNX
model.export(format='tflite')  # Exportar a TFLite
model.export(format='torchscript')  # Exportar a TorchScript
```

## Comandos útiles de OpenCV (cv2)

OpenCV es comúnmente usado con YOLO para procesamiento de imágenes y video:

```python
# Importar OpenCV
import cv2

# Leer imagen
img = cv2.imread('imagen.jpg')

# Mostrar imagen
cv2.imshow('Ventana', img)
cv2.waitKey(0)

# Redimensionar imagen
resized = cv2.resize(img, (640, 480))

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Guardar imagen
cv2.imwrite('nueva_imagen.jpg', img)

# Capturar video desde webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Dibujar rectángulo
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Dibujar texto
cv2.putText(img, "Texto", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
```

## Ejemplo completo: Detección con YOLO8 y OpenCV

```python
from ultralytics import YOLO
import cv2

# Cargar modelo
model = YOLO('yolov8n.pt')

# Abrir webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Leer frame
    ret, frame = cap.read()
    if not ret:
        break
        
    # Ejecutar inferencia
    results = model(frame)
    
    # Visualizar resultados
    res_plotted = results[0].plot()
    
    # Mostrar resultado
    cv2.imshow("YOLOv8 Detection", res_plotted)
    
    # Salir con 'q'
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
```