import os
def create_folder_structure(entity_name, category):
  os.makedirs(f"output/{entity_name}/{category}", exist_ok=True)
def build_filename(name, document_type, extension):
return f"{name}_{document_type}.{extension}"
