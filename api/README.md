# Flight Prediction API

## Description

Una vez realizado el entrenamiento y seleccionado en base a las metricas algún modelo a desplegar, la insercion de la API puede ser generada de 2 maneras.
En esta exposicion, se realizará mediante despliegue en cloud run, pero la herramienta MLFLOW permite le despliegue autogenerado por la herramienta misma.

---

## Structure  

The REST API file structure is the following: 

```bash
└── model
    ├── api.py
    ├── Dockerfile
    ├── requirements.txt
    ├── cloudbuild.yaml
    └── README.md 
```

* `api.py` - Script principal, el cual despliega via flask/gunicorn un endpoint para ejecutar predicciones.
* `Dockerfile` - utiliza una version de python3
* `requirements.txt` - archivos requeridos para compilacion de docker
* `cloudbuild.yaml` - archivo para despliegue para compilacion y creacion de servicio en cloud build

---

## Ejecucion

Para la ejecucion de estos scripts ocurre de manera automatizada al enviar el codigo fuente a los repositorios de cloud repository, estos mediante clodbuild despliegan un endpoint en cloud build en red interna o publica.
Cabe recalcar que para efectos de esta prueba, solo se generá la creacion de la API, con un metodo de validacion de ingesta basico, la seguridad está supervida por la nube en despliegue en este caso GCP y la opcion de autenticacion interna ademas
de la disponibilizacion de una VPC (fuera del alcance de esta prueba).

```bash
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 api:app
```

---

## REST request

Para obtener predicciones se requieren los siguientes componentes.

```bash
API_ENDPOINT/prediccion
```

El **API_ENDPOINT** es un valor de variable que posee el script de terraform.


Para generar la consulta via post se requiere un mensaje en formato JSON

```json
{
    "feature_vector": "0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1"
}
```

La key **feature_vector** debe poseer un valor de 37 digitos separados con , con valores 0 o 1.

---
## REST response

La respuesta de este servicio espera 2 valores, 0 o 1, el cual viene con un mensaje de la clase al a que pertenece.
(dentro de las mejoras propuestas, viene el almacenamiento de metada, por ejemplo nombre modelo, fecha, input y prediccion, esto debiera ser realizado en alguna base de datos transaccional para posterior monitoreo de performance de modelo (fuera del alcance de esta prueba)).

```json
{
    "predicted_class": "Delay",
    "prediction": 1
}
```


```json
{
    "predicted_class": "On time",
    "prediction": 0
}
```
