import pandas as pd
from typing import List, Optional
from model.location import Location

location_service_instance = None

def set_location_service(service):
    global location_service_instance
    location_service_instance = service

def get_location_service():
    return location_service_instance

class LocationService:
    def __init__(self, csv_path: str):
        # Leer el CSV con separación automática
        self.locations_df = pd.read_csv(csv_path, encoding='utf-8', sep=None, engine='python')

        # Limpiar nombres de columnas
        self.locations_df.columns = (
            self.locations_df.columns
            .str.strip()
            .str.lower()
            .str.replace("ó", "o")
            .str.replace(" ", "_")
        )

        # Renombrar columnas específicas si existen
        column_map = {
            "codigo_municipio": "codigo_municipio",
            "nombre_municipio": "nombre_municipio"
        }

        # Verificación robusta
        for key in column_map.keys():
            if key not in self.locations_df.columns:
                raise ValueError(f"Columna requerida no encontrada en CSV: {key}")

        # Extraer columnas necesarias
        self.locations_df = self.locations_df[list(column_map.values())].drop_duplicates()

    def get_all_locations(self) -> List[Location]:
        return [
            Location(code=int(row["codigo_municipio"]), description=row["nombre_municipio"])
            for _, row in self.locations_df.iterrows()
        ]

    def get_location_by_code(self, code: int) -> Optional[Location]:
        match = self.locations_df[self.locations_df["codigo_municipio"] == code]
        if not match.empty:
            row = match.iloc[0]
            return Location(code=int(row["codigo_municipio"]), description=row["nombre_municipio"])
        return None