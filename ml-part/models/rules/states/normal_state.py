from models.rules.states.elevated_state import ElevatedState

class NormalState:
    def handle(self, context):
        chol = float(context.data["chol"])
        if chol > 240:
            context.alerts.append("High cholesterol detected")
            context.set_state(ElevatedState())
            context.evaluate()