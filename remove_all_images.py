
import os

def remove_images():
    if os.path.exists("Analisi sensibilità"):
        print("Removing images...")
        cont = 0

        now_free_space = 0    

        cont_files = 0
        for root, dirs, files in os.walk("Analisi sensibilità"):
            for file in files:
                if file.endswith(".png") and ('costs' in file or 'simulation' in file):
                    cont_files += 1

        for root, dirs, files in os.walk("Analisi sensibilità"):
            for file in files:
                if file.endswith(".png") and ('costs' in file or 'simulation' in file):
                    now_free_space = (os.stat(os.path.join(root, file)).st_size) / (1024 * 1024)
                    print(f"Removing file {cont}/{cont_files}: {root}{file}")
                    os.remove(os.path.join(root, file))
                    cont += 1

        print(f"Removed {cont} images from {cont_files} images, now free space: {now_free_space} MB")




if __name__ == "__main__":
    remove_images()