
from vsg import rule
from vsg import fix

import re


class rule_024(rule.rule):
    '''
    Process rule 024 checks for a single space after the process label and the :.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'process'
        self.identifier = '024'
        self.solution = 'Ensure a single space exists between process label and :.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isProcessKeyword:
                if re.match('^\s*\S+\s*:', oLine.line):
                    if not re.match('^\s*\S+\s:', oLine.line):
                        self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_before_word(self, oFile.lines[iLineNumber], ':')
