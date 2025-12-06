import subprocess
import os
from pdf2image import convert_from_path

def ppt_to_images(workspace_root):
    temp_dir = os.path.join(workspace_root, "temp")
    
    # Find the most recent .ppt file
    ppt_files = [f for f in os.listdir(temp_dir) if f.endswith('.ppt')]
    if not ppt_files:
        raise FileNotFoundError("No .ppt file found in temp directory")
    
    # Get the most recent file
    ppt_files.sort(reverse=True)  # Sort by name (timestamp) descending
    ppt_file = os.path.join(temp_dir, ppt_files[0])
    
    pdf_file = os.path.join(workspace_root, "temp", "presentation.pdf")
    output_folder = os.path.join(workspace_root, "temp", "slide_images")

    # Try to find LibreOffice executable
    soffice_paths = [
        "soffice",  # If in PATH
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    
    soffice_exe = None
    for path in soffice_paths:
        if path == "soffice" or os.path.exists(path):
            soffice_exe = path
            break
    
    if not soffice_exe:
        raise FileNotFoundError("LibreOffice (soffice) not found. Please install LibreOffice.")
    
    print(f"Using LibreOffice at: {soffice_exe}")
    print(f"Converting: {ppt_file}")
    
    # Always use shell=True on Windows for better compatibility
    import sys
    if sys.platform == 'win32':
        # For Windows, always use shell=True
        command_str = f'"{soffice_exe}" --headless --convert-to pdf --outdir "{os.path.dirname(pdf_file)}" "{ppt_file}"'
        print(f"Running command: {command_str}")
        subprocess.run(command_str, shell=True, check=True)
    else:
        command = [
            soffice_exe,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", os.path.dirname(pdf_file),
            ppt_file
        ]
        subprocess.run(command, check=True)

    os.makedirs(output_folder, exist_ok=True)
    images = convert_from_path(pdf_file)
    image_paths = []
    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"slide_{i+1}.png")
        img.save(img_path, "PNG")
        image_paths.append(img_path)

    return image_paths
