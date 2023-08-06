
from vsg import rule
from vsg import check
from vsg import fix


class rule_005(rule.rule):
    '''
    Type rule 005 checks for the proper indentation of multiline types.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'type', '005')
        self.solution = 'Ensure proper indentation.'
        self.phase = 4

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.insideType and not oLine.isTypeKeyword and not oLine.isBlank:
                check.indent(self, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.indent(self, oFile.lines[iLineNumber])
