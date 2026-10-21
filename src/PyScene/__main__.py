import sys
import os

def main():
    args = sys.argv[1:]
    if not args:
        print("PyScene CLI Tools")
        print("Usage:")
        print("  python -m PyScene manager   - Launch tilemap & asset manager GUI")
        #print("  python -m PyScene clean     - Scan and remove orphaned engine files")
        return

    command = args[0].lower()
    
    if command == "manager":
        # Import and launch the PyGame GUI manager
        from PyScene.tools.manager_gui import ManagerGUI
        ManagerGUI()
        
    else:
        print(f"Unknown PyScene command: '{command}'")

if __name__ == "__main__":
    main()