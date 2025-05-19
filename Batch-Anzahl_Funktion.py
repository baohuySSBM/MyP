from itertools import product
import pandas as pd
from fastapi import FastAPI, HTTPException
from typing import Dict
from datetime import datetime


def batch_anzahl():
    erlaubte_einheiten = ["Stück", "Liter", "kg"]

    while True:
        batch_str = input(" Batchanzahl: ").strip()
        einheit = input(" Einheit (z.B. Stück, Liter, kg): ").strip()

        if not einheit:
            print(" ❌ Bitte gib eine Einheit ein (Stück, kg, Liter).")
            continue

        if einheit not in erlaubte_einheiten:
            print(f" ❌ Ungültige Einheit. Erlaubt sind: {', '.join(erlaubte_einheiten)}.")
            continue

        try:
            batch = int(batch_str)
            if batch <= 0:
                print(" ❌ Die Batch-Anzahl muss eine positive ganze Zahl sein.")
                continue
        except ValueError:
            print(" ❌ Ungültige Batchanzahl. Bitte eine ganze Zahl eingeben.")
            continue

        # Wenn alles korrekt:
        print(f"✅ Batchanzahl: {batch} {einheit}")
        return batch, einheit


if __name__ == "__main__":
    batch, einheit = batch_anzahl()
    print(f"✅ Ergebnis: {batch} {einheit}")
