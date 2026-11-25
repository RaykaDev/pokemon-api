from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Pokemon(Base):
    __tablename__ = "pokemons"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    altura: Mapped[int]
    peso: Mapped[int]
    tipo: Mapped[str]
