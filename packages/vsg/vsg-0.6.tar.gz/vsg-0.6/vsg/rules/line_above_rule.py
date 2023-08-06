
from vsg import fix
from vsg import check
from vsg import rule


class line_above_rule(rule.rule):

    def __init__(self, name=None, identifier=None, sTrigger=None):
        rule.rule.__init__(self, name, identifier)
        self.solution = 'Insert blank line above.'
        self.phase = 3
        # The user updates the attributes below
        self.condition = sTrigger

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.__dict__[self.condition]:
                check.is_blank_line_before(self, oFile, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations[::-1]:
            fix.insert_blank_line_above(self, oFile, iLineNumber)
