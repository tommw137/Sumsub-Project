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

if __name__ == "__main__":
    os.makedirs("test_downloads", exist_ok=True)
    open("test_downloads/dummy.pdf", "w").close()

    organize_document(
        entity_name="Acme Corp",
        category="KYB",
        name="Acme Corp",
        document_type="Articles of Association",
        source_path="test_downloads/dummy.pdf"
    )

  organize_document(
    entity_name="Acme Corp",
    category="KYC",
    name="John Doe",
    document_type="Passport",
    source_path="test_download/dummy.pdf"
  )

organize_document(
  entity_name="Acme Corp",
  category="KYC",
  subfolder="Jane Smith",
  name="Jane Smith",
  document_type="Utility Bill",
  source_path="test_download/dummy.pdf"
)
    
    print("Done! Check the output folder.")

