from models.rules.patient_context import PatientContext
from models.rules.states.normal_state import NormalState

def evaluate_rules(data):

    context = PatientContext(data)
    context.set_state(NormalState())
    context.evaluate()
    return context.alerts 
