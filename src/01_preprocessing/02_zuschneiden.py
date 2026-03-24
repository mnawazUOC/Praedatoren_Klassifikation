# Code zum Zuschneiden der Metadaten (Bilder)

import os
import cv2
import argparse

# --- Pfad-Konfiguration ---
current_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.abspath(os.path.join(current_dir, '../../data/processed'))
DEFAULT_OUTPUT = os.path.abspath(os.path.join(current_dir, '../../data/final'))


def zuschneiden(input_folder, output_folder, crop_percentage=0.12):
    # Sicherstellen, dass der Ausgabeordner existiert (Error-Prävention)
    os.makedirs(output_folder, exist_ok=True)

    # Anteil des Beschnitts am unteren Rand (crop Percentage)
    # 0.12 bedeutet, dass die unteren 12% des Bildes entfernt werden.

    # Liste aller Bilddateien im Verzeichnis abrufen
    image_files = []
    for file in os.listdir(input_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(file)

    print(f"Starte die Verarbeitung von {len(image_files)} Bildern")
    print(f"Die unteren {crop_percentage*100}% werden entfernt.")

    count = 0

    for filename in image_files:
        # 1) Pfade generieren
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 2) Bild einlesen (OpenCV liest Bilder als NumPy-Arrays)
        img = cv2.imread(input_path) # Zurückgeben: Höhe, Breite, 3 (Blue, Green, Red) oder None

        if img is None:
            print(f"Fehler: Datei {filename} konnte nicht gelesen werden.")
            continue

        # 3) Bilddimensionen abrufen (Höhe, Breite)
        height, width, _ = img.shape

        # 4) Neue Höhe berechnen (Originalhöhe - abzuschneidender Bereich)
        new_height = int(height * (1 - crop_percentage))

        # 5) Das Zuschneiden
        # Zur neuen Höhe, Breite
        cropped_img = img[0:new_height, 0:width]

        # 6) Bearbeitetes Bild speichern
        cv2.imwrite(output_path, cropped_img)
        count += 1

        # 7) Fortschrittsanzeige
        if count % 10 == 0: # Wenn Bilder 10 sind
            print(f"Verarbeitete Bilder: {count}")

    print("_" * 30)
    print(f"Fertig. Insgesamt {count} Bilder wurden im Ordner '{output_folder}' gespeichert.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Schneidet die untere Metadatenleiste von Wildtierkamerabildern ab."
    )
    parser.add_argument("--input", type=str, default=DEFAULT_INPUT,
                        help="Pfad zum Eingabeverzeichnis mit den Artenordnern")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT,
                        help="Pfad zum Ausgabeverzeichnis für zugeschnittene Bilder")
    args = parser.parse_args()

    # Iterate over all species directories
    species_list = [d for d in os.listdir(args.input)
                    if os.path.isdir(os.path.join(args.input, d))]

    if not species_list:
        print(f"Keine Tierarten-Ordner gefunden in '{args.input}'")
        exit(1)

    print(f"Gefundene Tierarten: {species_list}\n")

    for species in species_list:
        input_folder = os.path.join(args.input, species)
        output_folder = os.path.join(args.output, species)
        print(f"\n=== Verarbeite: {species} ===")
        zuschneiden(input_folder, output_folder)

    print("\n" + "=" * 40)
    print("Alle Verarbeitungen abgeschlossen.")