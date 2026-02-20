# 🏗️ BuildFlow: Construction Management System - Backend API

Este proyecto final del Bootcamp Fullstack, proporciona una solución robusta para la gestión de obras, asignaciones de personal y reportes en tiempo real. Este repo presenta el backend/API de dicho proyecto.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

## 👥 Proceso de Desarrollo
El proyecto fue desarrollado bajo una metodología **Agile**, realizando reuniones **Daily** para sincronización de tareas y utilizando **Notion** como centro de documentación y seguimiento de nuestro progreso.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.10+
* **Framework:** FastAPI
* **Base de Datos:** MySQL (arquitectura relacional)
* **Librerías Clave:** * `aiomysql` para operaciones asíncronas.
    * `PyJWT` para autenticación y seguridad de rutas.
    * `Pydantic` para validación de esquemas de datos.
* **Emailing:** Integración con servicio SMTP para notificaciones automáticas de asignación.

## 🚀 Características Principales
* **Sistema de Roles:** Gestión diferenciada entre Administradores y Operarios.
* **Lógica de Negocio Avanzada:** * Validación automática de disponibilidad de operarios (`status` logic).
    * Control de solapamiento de fechas en asignaciones.
    * Requiere supervisión de un Admin para iniciar proyectos de operarios.
* **Seguridad:** Endpoints protegidos mediante JWT (JSON Web Tokens).

## ⚙️ Instalación y Configuración
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv venv`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Configurar variables de entorno (`.env`) con las credenciales de la DB.
5. Ejecutar: `uvicorn main:app --reload`.

## 📦 Deploy
El backend está configurado para ejecutarse en contenedores/servidores compatibles con Python, integrándose perfectamente con el frontend para el flujo de datos.
