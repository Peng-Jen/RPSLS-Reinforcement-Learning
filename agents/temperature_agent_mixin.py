class TemperatureAgentMixin:
    def __init__(self, temperature, temperature_decay, temperature_min):
        self.temperature = temperature
        self.temperature_decay = temperature_decay
        self.temperature_min = temperature_min

    def decay_temperature(self):
        self.temperature = max(self.temperature_min, self.temperature * self.temperature_decay)
