"""Application module."""
import os.path
import pathlib

from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI,Request


from brokers_services.containers import FileProcessingContainer
from dependency_injector.wiring import inject
working_dir =str(pathlib.Path(__file__).parent.parent)

@inject
def register_processing(run,depend_containers=None)->FileProcessingContainer:
    container = FileProcessingContainer()
    container.init_resources()
    mdl_inject = [

        __name__,
        "__main__",
        run.__module__
    ]
    __injections__ =    run.__dict__.get('__injections__')
    wire_modules =[]
    for k,v in __injections__.items():
        wire_modules+=[v.cls.__module__]

    if depend_containers!=None:
        for c in depend_containers:
            if issubclass(c,DeclarativeContainer):
                fc=c()
                fc.init_resources()
                fc.wire(modules=wire_modules)
            mdl_inject+=[c.__module__]
    container.wire(modules=mdl_inject)

    return run



