from model.typedoc import Typedoc
import pandas as pd
from typing import List, Optional
import os

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
# Servicio de Departamentos (TypeDocs)
# -------------------------------
class TypedocService:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

        if os.path.exists(csv_path):
            self.departments_df = pd.read_csv(csv_path, encoding='utf-8', sep=',')
            self.departments_df.columns = self.departments_df.columns.str.strip()
        else:
            self.departments_df = pd.DataFrame(columns=["Código Departamento", "Nombre Departamento"])

        # Solo dejamos las columnas necesarias y eliminamos duplicados
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

    def add_typedoc(self, typedoc: Typedoc):
        new_row = {
            "Código Departamento": typedoc.code,
            "Nombre Departamento": typedoc.description
        }
        self.departments_df = pd.concat([self.departments_df, pd.DataFrame([new_row])], ignore_index=True)
        self.departments_df.drop_duplicates(inplace=True)
        self._save_to_csv()

    def _save_to_csv(self):
        self.departments_df.to_csv(self.csv_path, index=False, encoding='utf-8')