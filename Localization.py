from service.LocalizationService import LocalizationService


class Localization:
    localizationService = LocalizationService()

    def run(self):
        self.localizationService.sendMessage()

localization = Localization()
localization.run()
