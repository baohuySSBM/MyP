from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()
mhd_db = {}


class Product(BaseModel):
    name: str
    mhd: str

    @field_validator("mhd")
    @classmethod
    def validate_date(cls, value):
        try: 
            parsed_date = datetime.strptime(value, "%d.%m.%Y"). date()
        except ValueError:
            raise ValueError(" Ungültiges Datumformat. Bitte TT.MM.JJJJ verwenden")
        
        if parsed_date < datetime.now().date():
            raise ValueError("MHD darf nicht in der Vergangenheit liegen.")
        
        return parsed_date


@app.post("/mhd")
def add_or_update_product(product: Product):
    if not product.name.strip():
        raise HTTPException(status_code=400, detail="Produktname darf nicht leer sein.")

    if product.name in mhd_db:
        message = "⚠️ Produkt aktualisiert."
    else:
        message = "✅ Produkt gespeichert."

    mhd_db[product.name] = {"mhd": product.mhd}
    return {
        "message": message,
        "produkt": product.name,
        "mhd": product.mhd.strftime("%d.%m.%Y")
    }


@app.get("/mhd")
def get_all_products():
    if not mhd_db:
        return {"message": "🔎 Noch keine Produkte eingetragen."}
    return {
        "produkte": {
            name: {"mhd": daten["mhd"].strftime("%d.%m.%Y")}
            for name, daten in mhd_db.items()
        }
    }
