from model.location import Location
import pandas as pd
from typing import List, Optional

# -------------------------------
# Instancia global del servicio
# -------------------------------
location_service_instance = None

def set_location_service(service):
    global location_service_instance
    location_service_instance = service

def get_location_service():
    return location_service_instance

# -------------------------------
# Servicio de Location
# -------------------------------
class LocationService:
    def __init__(self, csv_path: str):
        self.locations_df = pd.read_csv(csv_path, encoding='latin1', sep=';')

    def get_all_locations(self) -> List[Location]:
        return [
            Location(code=int(row["Código Municipio"]), description=row["Nombre Municipio"])
            for _, row in self.locations_df.iterrows()
        ]

    def get_states(self) -> List[Location]:
        states = self.locations_df[["Código Departamento", "Nombre Departamento"]].drop_duplicates()
        return [
            Location(code=int(row["Código Departamento"]), description=row["Nombre Departamento"])
            for _, row in states.iterrows()
        ]

    def get_locations_by_state_code(self, state_code: int) -> List[Location]:
        filtered = self.locations_df[self.locations_df["Código Departamento"] == state_code]
        return [
            Location(code=int(row["Código Municipio"]), description=row["Nombre Municipio"])
            for _, row in filtered.iterrows()
        ]

    def get_location_by_code(self, location_code: int) -> Optional[Location]:
        match = self.locations_df[self.locations_df["Código Municipio"] == location_code]
        if not match.empty:
            row = match.iloc[0]
            return Location(code=int(row["Código Municipio"]), description=row["Nombre Municipio"])
        return None

    def get_capitals(self) -> List[Location]:
        capitals = self.locations_df[self.locations_df["Código Municipio"] % 100 == 1]
        return [
            Location(code=int(row["Código Municipio"]), description=row["Nombre Municipio"])
            for _, row in capitals.iterrows()
        ]