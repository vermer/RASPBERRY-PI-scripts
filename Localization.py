from service.LocalizationService import LocalizationService


class Localization:
    def __init__(self):
        pass

    localizationService = LocalizationService()

    def run(self):
        self.localizationService.sendMessage()

localization = Localization()
localization.run()
