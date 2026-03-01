from abc import ABC

class BaseDTO(ABC):
    def _translate_state(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in ("true", "on"):
                return True
            if normalized in ("false", "off"):
                return False
        raise TypeError('Campo "value" precisa ser boolean ou string válida')