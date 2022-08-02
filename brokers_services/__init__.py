"""Application module."""
import os.path
import pathlib

from fastapi import FastAPI,Request


from brokers_services.containers import FileProcessingContainer
from dependency_injector.wiring import inject
working_dir =str(pathlib.Path(__file__).parent.parent)

@inject
def register_processing(run)->FileProcessingContainer:
    container = FileProcessingContainer()
    container.init_resources()

    container.wire(modules=[

        __name__,
        "__main__",
        run.__module__
    ])

    return run



