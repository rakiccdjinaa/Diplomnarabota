from models.rules.states.high_risk_state import HighRiskState

class ElevatedState:
    def handle(self, context):
        oldpeak = float(context.data["oldpeak"])
        if oldpeak > 2:
            context.alerts.append("Possible ischemic changes")
            context.set_state(HighRiskState())
            context.evaluate()
        
        if float(context.data["trestbps"]) > 180:
            context.alerts.append("Severe hypertension crisis risk")
        
        if (
            float(context.data["chol"]) > 240
            and float(context.data["trestbps"]) > 140
            and float(context.data["fbs"]) == 1
        ):
            context.alerts.append("Metabolic syndrome risk detected")
