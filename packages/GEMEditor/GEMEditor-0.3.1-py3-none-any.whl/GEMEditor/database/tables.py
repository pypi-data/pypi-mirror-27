import os.path
from PyQt5.QtWidgets import QMessageBox, QDialogButtonBox
from GEMEditor.database import miriam_databases
from GEMEditor.database.base import DatabaseWrapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    mnx_prefix = Column(String)
    name = Column(String)
    type = Column(String)
    miriam_collection = Column(String)
    validator = Column(String)
    use_resource = Column(Boolean)


class Compartment(Base):
    __tablename__ = "compartments"

    id = Column(Integer, primary_key=True)
    mnx_id = Column(String)
    name = Column(String)


class Metabolite(Base):
    __tablename__ = 'metabolites'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    formula = Column(String)
    charge = Column(Integer)


class MetaboliteName(Base):
    __tablename__ = "metabolite_names"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolites.id"))
    name = Column(String)


class MetaboliteId(Base):
    __tablename__ = "metabolite_ids"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolites.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    identifier = Column(String)


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True)
    string = Column(String)


class ReactionName(Base):
    __tablename__ = "reaction_names"

    id = Column(Integer, primary_key=True)
    reaction_id = Column(Integer, ForeignKey("reactions.id"))
    name = Column(String)


class ReactionId(Base):
    __tablename__ = "reaction_ids"

    id = Column(Integer, primary_key=True)
    reaction_id = Column(Integer, ForeignKey("reactions.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    identifier = Column(String)


class ReactionMember(Base):
    __tablename__ = "reaction_participants"

    id = Column(Integer, primary_key=True)
    reaction_id = Column(Integer, ForeignKey("reactions.id"))
    metabolite_id = Column(Integer, ForeignKey("metabolites.id"))
    stoichiometry = Column(Float)
    compartment_id = Column(Integer, ForeignKey("compartments.id"))


class Pathway(Base):
    __tablename__ = "pathways"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    string = Column(String)


class PathwayName(Base):
    __tablename__ = "pathway_names"

    id = Column(Integer, primary_key=True)
    pathway_id = Column(Integer, ForeignKey("pathways.id"))
    name = Column(String)


class PathwayItem(Base):
    __tablename__ = "pathway_members"

    id = Column(Integer, primary_key=True)
    pathway_id = Column(Integer, ForeignKey("pathways.id"))
    reaction_id = Column(Integer, ForeignKey("reactions.id"))


def setup_resources(session):
    """ Setup the resource tables in the database

    Parameters
    ----------
    session: sqlalchemy.Session

    Returns
    -------
    None
    """
    for database in miriam_databases:
        new_resource = Resource(name=database.name,
                                miriam_collection=database.miriam_collection,
                                validator=database.validator,
                                mnx_prefix=database.mnx_prefix,
                                type=database.type,
                                use_resource=True)
        session.add(new_resource)
    session.commit()


def setup_empty_database(parent=None, database_path=None):

    if database_path is None:
        database_path = DatabaseWrapper.get_database_path()

    # Database already exists
    if os.path.isfile(database_path):
        status = QMessageBox().question(parent, "Database found",
                                        "It seems like there is already a database present.\n"
                                        "Would you like to delete the old database and generate a new one?")
        if status == QDialogButtonBox.No:
            return False
        elif status == QDialogButtonBox.Yes:
            try:
                os.remove(database_path)
            except OSError:
                QMessageBox().critical(parent, "Error deleting database",
                                       "Could not remove the existing database. Is it currently in use?")
                return False
        else:
            raise ValueError("Unknown status from question messagebox")

    # Setup the database engine
    engine = create_engine('sqlite:///{}'.format(database_path))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables
    setup_resources(session)
    session.close()
    return True
