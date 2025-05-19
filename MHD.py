from datetime import datetime, date
from fastapi import FastAPI, HTTPException

mhd_db = {}


def input_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
            if date < datetime.now().date():
                print(" ❌ Das Datum liegt in der Vergangenheit.")
                continue
            return date
        except ValueError:
            print(" ❌ Ungültiges Datumformat! Bitte TT.MM.JJJJ verwenden.")


def mhd_eintragen():
    product_name = input(" Produktname: ").strip()
    if not product_name:
        print(" ❌ Produktname darf nicht leer sein.")
        return

    mhd_datum = input_valid_date(" MHD (TT.MM.JJJJ): ")

    if product_name in mhd_db:
        print(f" ⚠️ Produkt '{product_name}' existiert bereits.")
        update = input(" Möchtest du das MHD aktualisieren? (j/n): ").lower().strip()
        if update != "j":
            print(" 🛑 Aktualisierung abgebrochen.")
            return

    print("\n Vorschau der Eingabe:")
    print(f"  - Produktname: {product_name}")
    print(f"  • MHD: {mhd_datum.strftime('%d.%m.%Y')}")

    bestätigen = input(" Möchtest du diese Daten speichern? (j/n): ").lower().strip()
    if bestätigen != "j":
        print(" Eingabe verworfen.")
        return

    mhd_db[product_name] = {"mhd": mhd_datum}
    print(f" ✅ MHD für '{product_name}' gespeichert oder aktualisiert.")


def anzeigen():
    if not mhd_db:
        print(" 🔎 Noch keine Produkte eingetragen.")
        return

    print("\n 📋 Alle eingetragenen Produkte:")
    for name, daten in mhd_db.items():
        print(f"  - Produktname: {name}")
        print(f"  • MHD: {daten['mhd'].strftime('%d.%m.%Y')}")


if __name__ == "__main__":
    while True:
        mhd_eintragen()
        weiter = input("\nNoch ein Produkt eintragen oder ändern? (j/n): ").lower()
        if weiter != "j":
            break

    anzeigen()
