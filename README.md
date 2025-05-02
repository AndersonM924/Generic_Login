# Generic Login Automation

Este proyecto automatiza el proceso de inicio de sesión en una página web utilizando Playwright con Python.

## 🚀 Requisitos Previos

- Python 3.x
- Git

## 🛠️ Instalación

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual**
   ```bash
   # En Windows
   venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar Chromium**
   ```bash
   playwright install chromium
   ```

## 📝 Configuración

1. Crea un archivo `.env` con las siguientes variables:
   ```env
   # Datos de acceso
   LOGIN_URL=https://tu-sitio-web.com
   USERNAME=tu-usuario
   PASSWORD=tu-contraseña

   # Selectores
   USER_SEL=#username
   PASS_SEL=#password
   BTN_SEL=button[type="submit"]

   # Opcional
   EXPAND_SEL=.selector-opcional
   ```

## ▶️ Uso

Para ejecutar el script:
```bash
python generic_login.py
```

## 📋 Notas
- Asegúrate de tener el entorno virtual activado antes de ejecutar el script
- Verifica que todas las variables en el archivo `.env` estén correctamente configuradas
- El script utiliza Playwright para la automatización del navegador
- El archivo `storage_state.json` se genera automáticamente durante la ejecución y almacena el estado de la sesión. Este archivo está excluido del control de versiones ya que puede contener información sensible y cambia frecuentemente
