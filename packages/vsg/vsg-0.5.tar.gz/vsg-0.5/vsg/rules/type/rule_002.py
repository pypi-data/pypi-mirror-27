
from vsg import rule
from vsg import utilities
from vsg import fix
from vsg import check


class rule_002(rule.rule):
    '''
    Type rule 002 checks the "type" keyword is lowercase.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'type'
        self.identifier = '002'
        self.solution = 'Lowercase "type" keyword.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isTypeKeyword:
                check.is_lowercase(self, utilities.get_first_word(oLine), iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.lower_case(self, oFile.lines[iLineNumber], 'type')
