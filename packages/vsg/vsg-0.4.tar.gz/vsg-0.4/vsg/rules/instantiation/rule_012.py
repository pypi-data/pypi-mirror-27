
from vsg.rules.instantiation import instantiation_rule

import copy


class rule_012(instantiation_rule):
    '''
    Instantiation rule 012 checks the instantiation declaration and
    "generic map" keywords are not on the same line.
    '''

    def __init__(self):
        instantiation_rule.__init__(self)
        self.identifier = '012'
        self.solution = 'Place "generic map" keywords on the next line by \
                         itself'
        self.phase = 1

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isInstantiationDeclaration and oLine.isInstantiationGenericKeyword:
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            oLine = oFile.lines[iLineNumber]
            iIndex = oLine.lineLower.find(' generic ')
            oFile.lines.insert(iLineNumber + 1, copy.deepcopy(oLine))
            oLine.update_line(oLine.line[:iIndex])
            oLine.isInstantiationGenericKeyword = False
            oLine = oFile.lines[iLineNumber + 1]
            oLine.update_line(oLine.line[iIndex:])
            oLine.isInstantiationDeclaration = False
