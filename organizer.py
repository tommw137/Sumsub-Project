import os
import shutil

# building filepath
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

# detect pending items
def detect_required_docs(nature_of_business):
    required = set()
    nob = nature_of_business.lower()
    
    if "crypto" in nob or "exchange" in nob or "trading" in nob or "forex" in nob or "broker" in nob or "msb" in nob or "money services" in nob:
        required.add("License")
        required.add("AML Policy")
        required.add("Crypto Forensics Tool")
    
    if "casino" in nob or "gambling" in nob:
      required.add("License")
      required.add("AML Policy")
      required.add("Flow of Funds")

    if "investment" in nob or "asset management" in nob or "fund" in nob:
      required.add("License")
      required.add("AML Policy")
  
    return list(required)

# missing documents checklist for pending items
def check_missing_docs(entity_name, provided_docs, nature_of_business):
    pending = []
    
    always_required = [
        "Articles of Association",
        "Shareholder Registry",
        "Proof of Address",
        "Source of Funds", # not required for payment processor onboards (Insert PSP entities here)
        "Sumsub Inspection Report",
        "Sumsub Watchlist Report"
    ]
    
    # check always required docs
    for doc in always_required:
        if doc not in provided_docs:
            pending.append(f"{entity_name}: {doc} not found")
    
    # check situational docs
    situational = detect_required_docs(nature_of_business)
    for doc in situational:
        if doc not in provided_docs:
            pending.append(f"{entity_name}: {doc} not found")
  
    return pending

# testing file path
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
        source_path="test_downloads/dummy.pdf"
    )

    organize_document(
        entity_name="Acme Corp",
        category="KYC",
        subfolder="Jane Smith",
        name="Jane Smith",
        document_type="Utility Bill",
        source_path="test_downloads/dummy.pdf"
    )

    provided = ["Articles of Association", "Proof of Address"]
    pending =  check_missing_docs("Acme Corp", provided, "crypto exchange and trading")

    if pending:
      print("\nPending Items:")
      for item in pending:
        print(f" - {item}")
  
    print("Done! Check the output folder.")

