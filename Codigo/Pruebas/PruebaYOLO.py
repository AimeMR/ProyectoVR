# Instalar python, reiniciar para actualizar PATH
# installar librerias "pip install ultralytics" 
# desinstalar pythorch "pip uninstall torch torchvision torchaudio -y"   
# revisar version de cuda e intsalat pythorch "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121   "
import cv2
from ultralytics import YOLO

# Cargar el modelo YOLOv8 pre-entrenado
model = YOLO('yolov8x.pt').to('cuda')  # Versión nano (más ligera y rápida)
# Alternativas: 'yolov8s.pt' (small), 'yolov8m.pt' (medium), 'yolov8l.pt' (large), 'yolov8x.pt' (extra large)

# Inicializar la cámara (0 es generalmente la cámara principal)
cap = cv2.VideoCapture(0)

# Configurar resolución (opcional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Verificar que la cámara se abrió correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
    exit()

while True:
    # Capturar frame por frame
    ret, frame = cap.read()
    
    # Verificar si el frame se capturó correctamente
    if not ret:
        print("Error: No se pudo capturar el frame")
        break
    
    # Procesar el frame con YOLO
    results = model(frame, device='cuda')
    

    
    # Visualizar los resultados en el frame
    annotated_frame = results[0].plot()
    
    # Mostrar el frame procesado
    cv2.imshow('YOLOv8 Detection', annotated_frame)
    
    # Salir si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   

# Para cada frame procesado, puedes acceder a los datos específicos:
for r in results:
    # Coordenadas de los cuadros delimitadores (x1, y1, x2, y2)
    boxes = r.boxes.xyxy.cpu().numpy()
    
    # Etiquetas de clase (índices numéricos)
    class_ids = r.boxes.cls.cpu().numpy().astype(int)
    
    # Puntuaciones de confianza (0-1)
    confidences = r.boxes.conf.cpu().numpy()
    
    # Para cada detección en este frame
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        confidence = confidences[i]
        class_id = class_ids[i]
        class_name = model.names[class_id]
        
        print(f"Objeto: {class_name}, Confianza: {confidence:.2f}, Posición: [{int(x1)}, {int(y1)}, {int(x2)}, {int(y2)}]")
        
        # Aquí puedes implementar tu lógica para RA basada en estas detecciones

# Al terminar, liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

