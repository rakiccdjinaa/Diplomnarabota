class PatientContext:
    def __init__(self, data):
        self.data = data
        self.alerts = []
        self.state = None
    
    def set_state(self,state):
        self.state = state
    
    def evaluate(self):
        self.state.handle(self)