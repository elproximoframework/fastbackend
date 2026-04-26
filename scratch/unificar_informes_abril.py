import os

def unify_md_files(directory_path, output_filename):
    # Get all .md files in the directory
    md_files = [f for f in os.listdir(directory_path) if f.endswith('.md') and f != output_filename]
    # Sort files to maintain potential chronological or alphabetical order
    md_files.sort()

    output_path = os.path.join(directory_path, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# Unificación de informes de lanzamientos - Abril 2026\n\n")
        outfile.write(f"Este archivo contiene la unificación de {len(md_files)} informes detectados en el directorio.\n\n")
        outfile.write("---\n\n")
        
        for filename in md_files:
            file_path = os.path.join(directory_path, filename)
            outfile.write(f"## Archivo: {filename}\n\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    # Ensure there is a newline between files
                    if not content.endswith('\n'):
                        outfile.write('\n')
                outfile.write(f"\n\n---\n\n")
            except Exception as e:
                outfile.write(f"**Error leyendo {filename}: {str(e)}**\n\n")
    
    print(f"Unificación completada. Archivo generado: {output_path}")

if __name__ == "__main__":
    target_dir = r"D:\YoutubeElProximoFrameworkEnElEspacio\Web\lanzamientos\abril"
    output_file = "informes_unificados_abril.md"
    unify_md_files(target_dir, output_file)
