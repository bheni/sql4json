"""
Base EvaluationEngine defines the interface for providing an engine used
to evaluate custom expressions.  Sub classes must override evaluate in
order to process custom expressions
"""


class EvaluationEngine(object):
    def evaluate(self, tokens, evaluation_param):
        raise NotImplementedError("evaluate not implemented")