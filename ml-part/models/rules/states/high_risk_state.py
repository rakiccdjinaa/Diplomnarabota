class HighRiskState:

    def handle(self, context):
        context.alerts.append("Patient classified as HIGH RISK")