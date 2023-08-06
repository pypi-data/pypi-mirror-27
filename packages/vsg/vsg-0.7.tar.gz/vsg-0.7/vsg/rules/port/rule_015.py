
from vsg import rule
from vsg import check
from vsg import fix


class rule_015(rule.rule):
    '''
    Port rule 015 checks the indentation of closing parenthesis for port maps.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'port', '015')
        self.solution = 'Ensure proper indentation.'
        self.phase = 4

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isEndPortMap and not oLine.isPortDeclaration:
                check.indent(self, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.indent(self, oFile.lines[iLineNumber])
