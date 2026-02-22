from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    zipcode = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    housenumber = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    unit = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    tenants = relationship("Tenant", back_populates="property")
    invoices = relationship("Invoice", back_populates="ref_property")

    def __repr__(self):
        return f"<Property(id={self.id}, zipcode={self.zipcode}, city={self.city}, street={self.street})>"


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    house_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    family_name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    amount_people = Column(Integer, nullable=False)

    property = relationship("Property", back_populates="tenants")
    invoices = relationship("Invoice", back_populates="ref_tenant")

    def __repr__(self):
        return f"<Tenant(id={self.id}, family_name={self.family_name}, surname={self.surname})>"


class InvoiceEntry(Base):
    __tablename__ = "invoice_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    internal_notes = Column(Text, nullable=True)

    invoice = relationship("Invoice", back_populates="listing")

    def __repr__(self):
        return f"<InvoiceEntry(id={self.id}, title={self.title}, amount={self.amount})>"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer, nullable=False)
    ref_tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    ref_property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    total = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)

    ref_tenant = relationship("Tenant", back_populates="invoices")
    ref_property = relationship("Property", back_populates="invoices")
    listing = relationship("InvoiceEntry", back_populates="invoice")

    def __repr__(self):
        return f"<Invoice(id={self.id}, date={self.date}, total={self.total})>"

