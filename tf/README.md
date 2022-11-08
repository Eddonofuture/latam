# Terraform

## Descricion

Se limita la habilitacion de servicios por efectos de tiempo.
- cloudbuild
- source code
- artifact registry
- cloudrun
- iam
- SA

## Structure  

Esta estructura fue creada para disponibilizar la infraestructura basica de esta prueba.

```bash
└── terraform
    ├── main.tf
    ├── variables.tf
    └── README.md
```

* `main.tf` - archivo principal para creacion ejecucion de 
* `variables.tf` - declares variables


En este caso la ejecucion es local, la ejecucion debiera ser ejecutada desde una terminal de confianza idealmente con alguna tecnica de BASTION.
a la vez controlando los ambientes con alguna variable o secret manager.

```bash
terraform apply -var="project=project-name" -auto-approve
```