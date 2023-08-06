
from vsg import rule
from vsg import check
from vsg import fix


class rule_009(rule.rule):
    '''
    Entity rule 009 checks for spaces before the "end" keyword.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'entity'
        self.identifier = '009'
        self.solution = 'Ensure proper indentation.'
        self.phase = 4

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isEndEntityDeclaration:
                check.indent(self, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.indent(self, oFile.lines[iLineNumber])
