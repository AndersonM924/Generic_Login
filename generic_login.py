"""
Script genérico de inicio de sesión con Playwright.
– Toma todos los parámetros de un archivo .env
– Admite un botón/expansor opcional para desplegar el formulario
– Conserva la página abierta al final para inspección manual
"""

import asyncio, os
from pathlib import Path
from dotenv import load_dotenv, set_key
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── Cargar .env y forzar que sus claves prevalezcan sobre el entorno ──
ENV_FILE = Path(".env")
ENV_FILE.touch(exist_ok=True)               # crea el archivo si no existe
load_dotenv(dotenv_path=ENV_FILE, override=True)

# ── Ayudante para pedir y guardar variables que falten ──
def need(var: str, prompt: str) -> str:
    val = os.getenv(var, "").strip()
    if val:
        return val
    val = input(prompt).strip()
    set_key(str(ENV_FILE), var, val)        # guarda/actualiza en .env
    return val

# ── Parámetros requeridos ─────────────────────────────────────────────
LOGIN_URL = need("LOGIN_URL", "URL de login: ")
USERNAME  = need("USERNAME",  "Usuario / correo: ")
PASSWORD  = need("PASSWORD",  "Contraseña: ")

USER_SEL  = need("USER_SEL",  "Selector CSS del campo usuario: ")
PASS_SEL  = need("PASS_SEL",  "Selector CSS del campo contraseña: ")
BTN_SEL   = need("BTN_SEL",   "Selector CSS del botón de login: ")

# ── Parámetro opcional: botón o fila que despliega el formulario ─────
EXPAND_SEL = os.getenv("EXPAND_SEL", "").strip()   # dejar vacío si no aplica

STORAGE = Path("storage_state.json")

# ────────────────────────────── Main ─────────────────────────────────
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        ctx = await browser.new_context(
            storage_state=str(STORAGE) if STORAGE.exists() else None
        )
        page = await ctx.new_page()

        print(f"➡️  Abriendo {LOGIN_URL}")
        await page.goto(LOGIN_URL, wait_until="domcontentloaded")

        # 1. Desplegar el panel si se especificó EXPAND_SEL
        if EXPAND_SEL:
            try:
                print(f"🔽  Clic en expansor ({EXPAND_SEL}) …")
                await page.click(EXPAND_SEL, timeout=6000)
            except PWTimeout:
                print("⚠️  Expansor no encontrado (se continúa).")

        # 2. Esperar campos visibles
        print("⌛  Esperando campos de credenciales…")
        await page.wait_for_selector(USER_SEL, timeout=15000)
        await page.wait_for_selector(PASS_SEL, timeout=15000)

        # 3. Rellenar y enviar
        print("⌨️  Rellenando usuario y contraseña…")
        await page.fill(USER_SEL, USERNAME)
        await page.fill(PASS_SEL, PASSWORD)

        print("🔐  Enviando...")
        await asyncio.gather(
            page.click(BTN_SEL),
            page.wait_for_load_state("networkidle")   # ajuste según el sitio
        )

        # 4. Guardar cookies / localStorage
        await ctx.storage_state(path=STORAGE)
        print(f"✅  Sesión guardada en {STORAGE}")

        # 5. Mantener la ventana abierta para inspección
        print("👀  Navegador en pausa para inspección manual (Ctrl‑C para salir).")
        await page.pause()     # Playwright UI

if __name__ == "__main__":
    asyncio.run(main())
