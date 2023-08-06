
from vsg import rule
from vsg import fix

import re


class rule_003(rule.rule):
    '''
    Sequential rule 003 checks for a single space before the "<=" keyword.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'sequential'
        self.identifier = '003'
        self.solution = 'Ensure a single space exists before the "<=" keyword.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isSequential:
                if not re.match('^.*\s+<=', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_before_word(self, oFile.lines[iLineNumber], '<=')
