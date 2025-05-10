from model.typedoc import Typedoc
import pandas as pd
from typing import List, Optional

# -------------------------------
# Instancia global del servicio
# -------------------------------
typedoc_service_instance = None

def set_typedoc_service(service):
    global typedoc_service_instance
    typedoc_service_instance = service

def get_typedoc_service():
    return typedoc_service_instance

# -------------------------------
# Servicio de Departamentos (usando el modelo Typedoc)
# -------------------------------
class TypedocService:
    def __init__(self, csv_path: str):
        # Leer el archivo con el separador correcto
        self.departments_df = pd.read_csv(csv_path, encoding='utf-8', sep=',')
        # Extraer columnas necesarias y quitar duplicados
        self.departments_df = self.departments_df[["Código Departamento", "Nombre Departamento"]].drop_duplicates()

    def get_all_typedocs(self) -> List[Typedoc]:
        return [
            Typedoc(
                code=int(row["Código Departamento"]),
                description=row["Nombre Departamento"]
            )
            for _, row in self.departments_df.iterrows()
        ]

    def get_typedoc_by_code(self, code: int) -> Optional[Typedoc]:
        match = self.departments_df[self.departments_df["Código Departamento"] == code]
        if not match.empty:
            row = match.iloc[0]
            return Typedoc(
                code=int(row["Código Departamento"]),
                description=row["Nombre Departamento"]
            )
        return None