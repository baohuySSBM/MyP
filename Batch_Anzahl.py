from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI() 

erlaubte_einheiten = ["Stück", "Liter", "kg"]
batch_db = []


class BatchInput(BaseModel):
    batch: int 
    einheit: str

    @field_validator("batch")
    @classmethod
    def validate_batch(cls, value):
        if value <= 0:
            raise ValueError(" Die Batch-Anzahl muss eine positive ganze Zahl sein.")

        return value

    @field_validator("einheit")
    @classmethod
    def validate_einheit(cls, value):
        if value not in erlaubte_einheiten:
            raise ValueError(f" Untültige einheit. Erlaubt sind: {', '.join(erlaubte_einheiten)}.")
        return value


@app.post("/batch")
def check_batch(data: BatchInput):
    if data.einheit == "Barrel":
        raise HTTPException(status_code=501, detail="Einheit 'Barrel' wird nocht nicht unterstützt.")

    batch_db.append({"batch": data.batch, "einheit": data.einheit})

    return{
        "message": "✅ Eingabe gültig.",
        "batch": data.batch,
        "einheit": data.einheit
    }


@app.get("/batches")
def get_all_batches():
    if not batch_db:
        return {"message": " Keine Batches vorhanden."}

    return {"batches": batch_db}
