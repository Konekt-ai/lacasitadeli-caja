#!/usr/bin/env python3
"""
Script de configuración — La Casita POS
Instala dependencias y prepara la base de datos Neon
"""

import subprocess
import sys
import os

from dotenv import load_dotenv

load_dotenv("apps/api/.env")

def instalar_dependencias():
    print("📦 Instalando pymssql y python-dotenv...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pymssql", "python-dotenv"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("   ✅ Dependencias instaladas correctamente")
        return True
    else:
        print(f"   ❌ Error: {result.stderr}")
        return False

def probar_conexion():
    print("\n🔌 Probando conexión a SQL Server...")
    try:
        import pymssql
        server = os.environ.get("MSSQL_SERVER", r"localhost\SQLEXPRESS")
        database = os.environ.get("MSSQL_DATABASE", "novacaja22")
        user = os.environ.get("MSSQL_USER", "sa")
        password = os.environ.get("MSSQL_PASSWORD", "TuPassword")
        port = os.environ.get("MSSQL_PORT", "1433")

        conn = pymssql.connect(
            server=server,
            user=user,
            password=password,
            database=database,
            port=port,
            login_timeout=10
        )
        cur = conn.cursor()
        cur.execute("SELECT @@VERSION")
        version = cur.fetchone()[0]
        print(f"   ✅ Conectado a: {str(version)[:60]}...")
        conn.close()
        return True
    except Exception as e:
        print(f"   ❌ No se pudo conectar: {e}")
        print("   ⚠️  La app funcionará en modo offline con datos de prueba")
        return False

def main():
    print("=" * 55)
    print("  La Casita Delicatessen — Configuración del Sistema")
    print("=" * 55)

    ok_pip = instalar_dependencias()
    
    if ok_pip:
        probar_conexion()

    print("\n" + "=" * 55)
    print("  ✅ Configuración completada")
    print("  → Para iniciar: python caja.py")
    print("=" * 55)

if __name__ == "__main__":
    main()
