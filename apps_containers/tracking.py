from dependency_injector import containers, providers

import exten_services.tracking


class TrackingContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[

        "__main__"

    ])
    tracking:exten_services.tracking.TrackingService = providers.Factory(
        exten_services.tracking.TrackingService
    )



