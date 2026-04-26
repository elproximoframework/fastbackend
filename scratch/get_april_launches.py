from app.database import SessionLocal
from app.models import Launch, Rocket, Company
from datetime import datetime
import os

def get_april_launches():
    db = SessionLocal()
    try:
        # April 2026
        start_date = datetime(2026, 4, 1)
        end_date = datetime(2026, 5, 1)
        
        launches = db.query(Launch).filter(
            Launch.net >= start_date,
            Launch.net < end_date
        ).order_by(Launch.net).all()
        
        if not launches:
            print("No se encontraron lanzamientos en abril de 2026.")
            return

        md_content = "# Lanzamientos de Abril 2026\n\n"
        md_content = "# Lanzamientos de Abril 2026\n\n"
        
        # Prepare data for padding
        data = []
        headers = ["Fecha (NET)", "Nombre", "Cohete", "Proveedor", "Estado", "Misión"]
        
        for l in launches:
            r_name = (l.rocket.name if l.rocket else "N/A").strip()
            p_name = (l.provider.name if l.provider else "N/A").strip()
            d_str = (l.net.strftime("%Y-%m-%d %H:%M") if l.net else "N/A").strip()
            st = (l.status if l.status else "N/A").strip()
            
            # Replace internal pipes with slash to avoid breaking MD table
            # Replace all sorts of newlines and tabs
            name = l.name.replace("|", "/").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
            r_name = r_name.replace("|", "/").replace("\n", " ").replace("\r", " ").replace("\t", " ")
            p_name = p_name.replace("|", "/").replace("\n", " ").replace("\r", " ").replace("\t", " ")
            st = st.replace("|", "/").replace("\n", " ").replace("\r", " ").replace("\t", " ")
            
            miss = (l.mission_description or "N/A").replace("|", "/").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
            
            data.append([d_str, name, r_name, p_name, st, miss])
            
        # Calculate column widths for padding (optional for MD but makes it "square")
        widths = [len(h) for h in headers]
        for row in data:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(cell))
        
        # Build the table
        def format_row(row):
            return "| " + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) + " |\n"
            
        md_content += format_row(headers)
        md_content += "| " + " | ".join("-" * widths[i] for i in range(len(widths))) + " |\n"
        
        for row in data:
            md_content += format_row(row)
            
        # --- New task: Create individual files ---
        # Base directory: d:\YoutubeElProximoFrameworkEnElEspacio\Web\lanzamientos\abril
        # __file__ is in Web/backendfast/scratch/
        web_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        base_dir = os.path.join(web_root, "lanzamientos", "abril")
        os.makedirs(base_dir, exist_ok=True)
        
        for l in launches:
            date_str_file = l.net.strftime("%Y-%m-%d") if l.net else "unknown-date"
            # Sanitize name for filename
            clean_name = "".join(c if c.isalnum() else "_" for c in l.name).strip("_")
            # Include ID to avoid collisions
            filename = f"{date_str_file}_{clean_name}_{l.id}.md"
            filepath = os.path.join(base_dir, filename)
            
            # Detailed content for each file
            detail_content = f"# Lanzamiento: {l.name}\n\n"
            detail_content += f"**Fecha (NET):** {l.net.strftime('%Y-%m-%d %H:%M') if l.net else 'N/A'}\n"
            detail_content += f"**Cohete:** {l.rocket.name if l.rocket else 'N/A'}\n"
            detail_content += f"**Proveedor:** {l.provider.name if l.provider else 'N/A'}\n"
            detail_content += f"**Estado:** {l.status}\n"
            detail_content += f"**Misión:** {l.name_mission or 'N/A'}\n"
            detail_content += f"**Tipo de Misión:** {l.mission_type or 'N/A'}\n"
            detail_content += f"**Órbita:** {l.orbit_name or 'N/A'}\n"
            detail_content += f"**Plataforma de Lanzamiento:** {l.pad_name or 'N/A'} ({l.pad_location or 'N/A'})\n\n"
            detail_content += "## Descripción de la Misión\n"
            detail_content += f"{l.mission_description or 'No hay descripción disponible.'}\n\n"
            
            if l.image:
                detail_content += f"![Imagen del Lanzamiento]({l.image})\n\n"
                
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(detail_content)
        
        print(f"Creados {len(launches)} archivos individuales en {base_dir}")

    finally:
        db.close()

if __name__ == "__main__":
    get_april_launches()
