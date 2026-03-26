# Prácticas de Migración de Base de Datos

Este documento resume las recomendaciones sobre el flujo de actualización de la base de datos entre el entorno local y remoto (Railway).

## Análisis del Flujo Actual

El uso de un script de migración manual (`migrate_db.py`) es una forma efectiva y rápida para la etapa de desarrollo y prototipado.

### ✅ Ventajas
- **Agilidad**: Cambios instantáneos en la nube sin procesos complejos.
- **Control**: Conocimiento exacto de los datos transferidos y limpieza previa de la base de datos remota.
- **Consistencia**: Asegura que el entorno local y el remoto sean idénticos visualmente.

### ⚠️ Consideraciones de Crecimiento
- **Seguridad**: Evitar incluir contraseñas directamente en el código. Se recomienda usar variables de entorno (como `os.getenv("DATABASE_URL")`).
- **Peligro del `TRUNCATE`**: El comando `TRUNCATE` borra todos los datos existentes. En producción, esto eliminaría datos reales de usuarios.
- **Cambios de Esquema**: El script migra **datos**, pero no **estructura**. Si cambias una tabla (añades columnas), ambos entornos deben actualizarse primero.

## 🚀 Recomendaciones a Futuro

### 1. Migraciones de Esquema (Alembic)
Para proyectos que crecen, se recomienda usar **Alembic** junto con SQLAlchemy. Permite realizar cambios en la estructura de las tablas (añadir columnas, cambiar tipos) de forma segura y versionada.

### 2. Semillas de Datos (Seeds)
Utilizar scripts que carguen datos desde archivos fuente (como `load_data.py` con archivos `.ts`) es mejor a largo plazo, ya que el código se convierte en la "fuente de la verdad".

### 3. Migraciones de Gran Volumen
Para bases de datos con millones de registros, es preferible utilizar herramientas oficiales de PostgreSQL:
- `pg_dump`: Para exportar la base de datos.
- `pg_restore`: Para importarla en el servidor remoto.

---
*Documento generado para el portal de lanzamientos espaciales - Marzo 2026*
