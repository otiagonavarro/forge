class ForgeError(Exception):
    """Base error for all Forge domain failures."""


class ManifestNotFoundError(ForgeError):
    pass


class ManifestInvalidError(ForgeError):
    pass


class BlueprintNotFoundError(ForgeError):
    pass


class ComponentNotFoundError(ForgeError):
    pass


class DependencyCycleError(ForgeError):
    pass


class EngineNotFoundError(ForgeError):
    pass


class ActionError(ForgeError):
    def __init__(self, action_name: str, message: str):
        self.action_name = action_name
        super().__init__(f"{action_name}: {message}")
