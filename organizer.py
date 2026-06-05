import os
import shutil

def create_folder_structure(entity_name, category, subfolder=None):
  if subfolder:
    os.makedirs(f"output/{entity_name}/{category}/{subfolder}", exist_ok=True)
    return f"output/{entity_name}/{category}/{subfolder}"
  else:
    os.makedirs(f"output/{entity_name}/{category}", exist_ok=True)
    return f"output/{entity_name}/{category}"
def build_filename(name, document_type, extension):
  return f"{name}_{document_type}.{extension}"

def organize_document(entity_name, category, name, document_type, source_path, subfolder=None):
  extension = source_path.split(".")[-1]
  folder = create_folder_structure(entity_name, category, subfolder)
  filename = build_filename(name, document_type, extension)
  shutil.copy(source_path, os.path.join(folder, filename))
