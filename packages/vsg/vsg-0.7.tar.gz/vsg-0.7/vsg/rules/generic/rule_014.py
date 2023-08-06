
from vsg import rule
from vsg import fix

import re


class rule_014(rule.rule):
    '''Generic rule 014 checks for at least a single space before the :.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'generic'
        self.identifier = '014'
        self.solution = 'Add a space before the :.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isGenericDeclaration:
                if re.match('^\s*\S+\s*:\s*\S+\s*:=', oLine.line):
                    if not re.match('^\s*\S+\s+:', oLine.line):
                        self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_before_word(self, oFile.lines[iLineNumber], ':')
