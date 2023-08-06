
from vsg import rule
from vsg import fix

import re


class rule_005(rule.rule):
    '''
    Signal rule 005 checks there is a single space after the colon.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'variable'
        self.identifier = '005'
        self.solution = 'Ensure only a variable space after the colon.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isVariable:
                if not re.match('^\s*variable\s+.*\s*:\s\S', oLine.lineLower):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], ':')
