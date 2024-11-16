import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from pydot import Dot
from sqlalchemy_schemadisplay import create_schema_graph

from models import Base
from utils import get_engine


def create_diagram():
    graph: Dot = create_schema_graph(
        engine=get_engine(),
        metadata=Base.metadata,
        show_datatypes=False,
        show_indexes=False,
        rankdir="LR",
        concentrate=False,
    )
    graph.write_png("schema_diagram.png")


if __name__ == "__main__":
    create_diagram()
