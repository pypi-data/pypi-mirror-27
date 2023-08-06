
from vsg import rule
from vsg import check
from vsg import fix
from vsg import line


class rule_023(rule.rule):
    '''
    Architecture rule 023 ensures the alignment of comments.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'architecture'
        self.identifier = '023'
        self.solution = 'Inconsistent alignment of comments.'
        self.phase = 6

    def analyze(self, oFile):
        lGroup = []
        fGroupFound = False
        iStartGroupIndex = None
        for iLineNumber, oLine in enumerate(oFile.lines):
            if not fGroupFound and oLine.isArchitectureKeyword:
                fGroupFound = True
                iStartGroupIndex = iLineNumber
            if oLine.isArchitectureBegin:
                lGroup.append(oLine)
                fGroupFound = False
                check.keyword_alignment(self, iStartGroupIndex, '--', lGroup)
                lGroup = []
                iStartGroupIndex = None
            if fGroupFound:
                if oLine.hasComment and not oLine.isComment:
                    lGroup.append(oLine)
                else:
                    lGroup.append(line.line('Removed line'))

    def _fix_violations(self, oFile):
        fix.keyword_alignment(self, oFile)
