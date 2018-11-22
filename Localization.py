from service.LocalizationService import LocalizationService


class Localization:
    def __init__(self):
        pass

    def run(self):
        localizationService = LocalizationService()
        localizationService.run()


localization = Localization()
localization.run()
