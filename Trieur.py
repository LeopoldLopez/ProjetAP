import os
import shutil
import random

# Définition des chemins
data_dir = "/Users/gabri/OneDrive/moi/cours/ENSEEIHT/S8/ApprentissageProfond/ProjetFinal/ProjetAP/Données_Brutes"
# data_dir = "/Users/anishan/Desktop/GIT-DEEPVF/Données_Brutes"
sorted_data_dir = os.path.join(os.path.dirname(data_dir), "Données_Triée")
train_dir = os.path.join(sorted_data_dir, "train")
validation_dir = os.path.join(sorted_data_dir, "validation")
test_dir = os.path.join(sorted_data_dir, "test")
train_percentage = 0.7
validation_percentage = 0.15

# Création du répertoire Données_Triée s'il n'existe pas
os.makedirs(sorted_data_dir, exist_ok=True)

# Création des dossiers train, validation et test dans Données_Triée
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Dictionnaire pour stocker le nombre d'images pour chaque classe
image_counts = {}

# Parcours des dossiers de fleurs
for flower_class in os.listdir(data_dir):
    class_dir = os.path.join(data_dir, flower_class)
    if os.path.isdir(class_dir) and not flower_class.startswith(".git"):  # Exclure les répertoires commençant par ".git"
        # Liste des fichiers dans le dossier de la classe
        files = os.listdir(class_dir)
        # Mélange aléatoire des fichiers
        random.shuffle(files)
        # Calcul du nombre de fichiers pour chaque ensemble
        num_files = len(files)
        num_train = int(train_percentage* num_files)
        num_validation = int(validation_percentage * num_files)
        num_test = num_files - num_train - num_validation
        # Création des dossiers pour chaque classe
        train_class_dir = os.path.join(train_dir, flower_class)
        validation_class_dir = os.path.join(validation_dir, flower_class)
        test_class_dir = os.path.join(test_dir, flower_class)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(validation_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)
        # Copie des fichiers dans les dossiers train, validation et test
        for i, file in enumerate(files):
            src = os.path.join(class_dir, file)
            if i < num_train:
                dst = os.path.join(train_class_dir, file)  
            elif i < num_train + num_validation:
                dst = os.path.join(validation_class_dir, file) 
            else:
                dst = os.path.join(test_class_dir, file)  
            shutil.copy(src, dst)
        # Stocker le nombre d'images pour chaque classe
        image_counts[flower_class] = {'train': num_train, 'validation': num_validation, 'test': num_test, 'total': num_files}

# Affichage du nombre et du pourcentage d'images pour chaque type de fleur dans chaque dossier
print("Répartition des images par type de fleur :")
for flower_class, counts in image_counts.items():
    print(f"Fleur : {flower_class}")
    for dataset, count in counts.items():
        percentage = count / counts['total'] * 100
        print(f"- {dataset.capitalize()} : {count}/{counts['total']} images ({percentage:.2f}%)")
    print()
