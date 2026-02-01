from datetime import time

class BusinessHours:
    def __init__(self, day: str, open_at: time | None, close_at: time | None, active: bool):
        if day not in {
            "segunda-feira", "terca-feira", "quarta-feira",
            "quinta-feira", "sexta-feira", "sabado", 
            "domingo", "feriado"
        }:
            raise ValueError("Dia da semana inválido")

        if active:
            if open_at is None or close_at is None:
                raise ValueError(f"Horário obrigatório para {day}")

        self.day = day
        self.open_at = open_at
        self.close_at = close_at
        self.active = active

    def is_overnight(self):
        if not self.active:
            return False
        return self.close_at <= self.open_at

    def to_dict(self):
        return {
            "day": self.day,
            "active": self.active,
            "open_at": self.open_at.strftime("%H:%M") if self.open_at else None,
            "close_at": self.close_at.strftime("%H:%M") if self.close_at else None
        }

    def is_open(self):
        return self.active and self.open_at is not None and self.close_at is not None
