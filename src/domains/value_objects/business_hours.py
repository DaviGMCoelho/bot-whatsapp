from datetime import time

class BusinessHours:
    def __init__(self, day: str, opens_at: time | None, closes_at: time | None, active: bool):
        if day not in {
            "segunda-feira", "terca-feira", "quarta-feira",
            "quinta-feira", "sexta-feira", "sabado", 
            "domingo", "feriado"
        }:
            raise ValueError("Dia da semana inválido")

        if active:
            if opens_at is None or closes_at is None:
                raise ValueError(f"Horário obrigatório para {day}")

        self.day = day
        self.opens_at = opens_at
        self.closes_at = closes_at
        self.active = active

    def is_overnight(self):
        if not self.active:
            return False
        return self.closes_at <= self.opens_at

    def to_dict(self):
        return {
            "day": self.day,
            "active": self.active,
            "opens_at": self.opens_at.strftime("%H:%M") if self.opens_at else None,
            "closes_at": self.closes_at.strftime("%H:%M") if self.closes_at else None
        }

    def is_open(self):
        return self.active and self.opens_at is not None and self.closes_at is not None
