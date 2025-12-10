import os
import pickle
import glob

def load_latest_model():
    """Load the latest trained model from models/ folder"""
    models_dir = "models"
    
    if not os.path.exists(models_dir):
        print("⚠ No models directory found. Run: python one_timer/create_syllab_iq_model.py")
        return None
    
    # Find all .pkl files
    model_files = glob.glob(os.path.join(models_dir, "syllab_iq_*.pkl"))
    
    if not model_files:
        print("⚠ No trained models found. Run: python one_timer/create_syllab_iq_model.py")
        return None
    
    # Load the latest model (by modification time)
    latest_model_file = max(model_files, key=os.path.getmtime)
    
    try:
        with open(latest_model_file, "rb") as f:
            vector_manager = pickle.load(f)
        print(f"✓ Loaded model from '{latest_model_file}'")
        return vector_manager
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None