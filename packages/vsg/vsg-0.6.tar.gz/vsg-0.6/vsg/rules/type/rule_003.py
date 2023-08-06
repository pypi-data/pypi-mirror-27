
from vsg import rule
from vsg import fix

import re


class rule_003(rule.rule):
    '''
    Type rule 003 checks there is a single space after the "type" keyword.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'type'
        self.identifier = '003'
        self.solution = 'Remove all but one space after the "type" keyword.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isTypeKeyword:
                if not re.match('^\s*type\s\w', oLine.lineLower):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'type')
