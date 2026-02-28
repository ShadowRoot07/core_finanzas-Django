# 💰 Core Finanzas - Sistema de Gestión Contable

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon.tech-4169E1?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel)
![Pytest](https://img.shields.io/badge/Pytest-Verified-0E7FBF?style=for-the-badge&logo=pytest)

**Core Finanzas** es una aplicación robusta diseñada para el control total de las finanzas personales. Permite gestionar ingresos, gastos y cuentas bancarias con una arquitectura limpia y preparada para el despliegue escalable.

---

## 🚀 Demo En Vivo
Puedes probar la aplicación en el siguiente enlace:
👉 **[https://core-finanzas-django.vercel.app/]**

### 🔓 Acceso de Prueba (Invitado)
Para una revisión rápida, utiliza las siguientes credenciales:
- **Usuario:** `invitado`
- **Contraseña:** `finanzas2026`

---

## 📸 Vista Previa
> **Instrucciones para imágenes:** Sube tus capturas a una carpeta llamada `/screenshots` en tu repo y reemplaza los enlaces abajo.

| Dashboard Principal | Reportes y Gráficos |
| :---: | :---: |
| ![Dashboard](`![Dashboard](./media/Screenshot_20260228_133517.jpg)`) | ![Reportes](`![Reportes](./media/Screenshot_20260228_133520.jpg)`) |
| *Vista general de saldo y transacciones* | *Análisis de gastos por categoría* |

---

## ✨ Características Principales
- ✅ **Gestión de Transacciones:** Registro detallado de ingresos y gastos.
- 📊 **Dashboard Dinámico:** Visualización de gastos por categoría mediante gráficos.
- 🏦 **Multi-Cuentas:** Soporte para diferentes fuentes de dinero (Efectivo, Bancos, etc.).
- 📂 **Exportación de Datos:** Descarga de reportes financieros en formatos **CSV** y **PDF**.
- 🧪 **Testing Suite:** Cobertura de pruebas unitarias con `pytest` para servicios lógicos.
- 🎨 **UI Moderna:** Interfaz responsiva construida con Tailwind CSS.

---

## 🛠️ Stack Tecnológico
- **Backend:** Python 3.12 + Django 6.0 (MVT Architecture).
- **Database:** PostgreSQL alojado en **Neon.tech**.
- **Static Files:** WhiteNoise para el manejo eficiente de CSS/JS en producción.
- **Servidor Web:** Gunicorn.
- **Infraestructura:** Docker (Contenerización) y Vercel (Cloud Deployment).

---

## 🐳 Ejecución con Docker
Si deseas correr este proyecto localmente usando Docker, sigue estos pasos:

1. **Construir la imagen:**
   ```bash
   docker build -t core-finanzas-shadowroot07 .
    ```

2. **Ejecutar el contenedor:**
    ```bash
    docker run -d -p 8000:8000 --env-file .env core-finanzas-shadowroot07
    ```

## Configuración de Desarrollo
Para clonar y ejecutar localmente sin Docker:

* Clonar repositorio: git clone [URL_DE_TU_REPO]
* Instalar dependencias: pip install -r requirements.txt
* Variables de Entorno: Crea un archivo .env con:
* DATABASE_URL=postgres://tu_usuario:tu_pass@tu_host/tu_db
* SECRET_KEY=tu_clave_secreta
* DEBUG=True
* Migraciones: python manage.py migrate
* Servidor: python manage.py runserver

## 👤 Autor
*Desarrollado por ShadowRoot07.*
Programador apasionado por la eficiencia y el código limpio.
