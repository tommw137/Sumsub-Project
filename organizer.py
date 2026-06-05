import os
def create_folder_structure(entity_name, category):
  os.makedirs(f"output/{entity_name}/{category}", exist_ok=True)
