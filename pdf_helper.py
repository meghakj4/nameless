import os

def load_pdfs_on_startup(vector_manager):
    """Load and store PDFs before chatbot starts. Returns True on success."""
    print("=" * 50)
    print("PDF Learning Phase")
    print("=" * 50)
    print()
    
    pdf_files = []
    pdfs_folder = "pdfs"
    if os.path.exists(pdfs_folder):
        for filename in os.listdir(pdfs_folder):
            if filename.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(pdfs_folder, filename))
    
    specific_pdf = r"C:\Users\Megha\Downloads\MOD5_Notes.pdf"
    if os.path.exists(specific_pdf):
        pdf_files.append(specific_pdf)
    
    if not pdf_files:
        print("⚠ No PDF files found!")
        print(f"Please place PDFs in '{pdfs_folder}/' folder or check the path.")
        print()
        add_more = input("Do you want to add a PDF manually? (yes/no): ").strip().lower()
        if add_more == 'yes':
            pdf_path = input("Enter PDF file path: ").strip()
            if os.path.exists(pdf_path):
                pdf_files.append(pdf_path)
            else:
                print(f"Error: File not found at {pdf_path}")
                return False
        else:
            print("Starting chatbot without any PDFs...\n")
            return True
    
    print(f"Found {len(pdf_files)} PDF file(s). Loading...\n")
    for pdf_path in pdf_files:
        print(f"Loading: {os.path.basename(pdf_path)}")
        success = vector_manager.add_pdf_to_store(pdf_path)
        if not success:
            print(f"Failed to load: {pdf_path}\n")
        else:
            print()
    
    info = vector_manager.get_store_info()
    print(f"\n{info}")
    print("=" * 50)
    print("PDF Learning Complete! Ready to chat.\n")
    print()
    return True