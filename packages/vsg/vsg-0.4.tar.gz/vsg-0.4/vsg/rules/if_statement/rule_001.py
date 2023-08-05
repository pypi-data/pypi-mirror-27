
from vsg.rules.if_statement import if_rule
from vsg import check
from vsg import fix


class rule_001(if_rule):
    '''If rule 001 checks for the proper indentation at the beginning of the line.'''

    def __init__(self):
        if_rule.__init__(self)
        self.identifier = '001'
        self.solution = 'Ensure proper indentation.'
        self.phase = 4

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isIfKeyword or oLine.isElseIfKeyword or oLine.isEndIfKeyword or oLine.isElseKeyword:
                check.indent(self, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.indent(self, oFile.lines[iLineNumber])
