from dataclasses import dataclass
from typing import Optional

@dataclass
class Property:
    id: Optional[int]
    zipcode: str
    city: str
    street: str
    housenumber: str
    floor: int
    unit: int
    description: str

@dataclass
class Tenant:
    id: Optional[int]
    house_id: int
    family_name: str
    surname: str
    start_date: str
    end_date: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    amount_people: int

@dataclass
class InvoiceEntry:
    title: str
    amount: float
    internal_notes: Optional[str]

@dataclass
class Invoice:
    id: Optional[int]
    date: int
    ref_tenant: Tenant
    ref_property: Property
    total: float
    listing: [InvoiceEntry]
    notes: str

