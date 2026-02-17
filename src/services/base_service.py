from abc import ABC

class BaseService(ABC):
    def _translate_state(self, raw_state: str):
        if not isinstance(raw_state, str):
            raise ValueError("Estado inválido")
        state = raw_state.lower()

        if state in ("on", "true", "1"):
            return True
        if state in ("off", "false", "0"):
            return False
        raise ValueError("Estado inválido")
