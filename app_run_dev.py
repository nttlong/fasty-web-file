from dependency_injector.wiring import inject, Provide

import web_hosting.templates.single_page_apps
import web_hosting.models.statics
from fasty_containers.app import ContainerApp
@inject
def start(
        web_app=Provide[ContainerApp.web_app],
        static:web_hosting.models.statics.HostModel_Static = Provide[ContainerApp.host_model_static],
        spa = Provide[ContainerApp.host_model_spa]
):
    static.start()
    web_app.start()

@inject
def run():
    application = ContainerApp()
    application.init_resources()
    application.wire(modules=[
        __name__,
        # web_hosting.templates.single_page_apps.__name__
    ])
    start()
    # application.web_app.start()


if __name__=="__main__":
    run()
