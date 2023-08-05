
from vsg.rules.process import process_rule
from vsg import fix

import re


class rule_007(process_rule):
    '''
    Process rule 007 checks for a single space between the "end" and "process" keywords.
    '''

    def __init__(self):
        process_rule.__init__(self)
        self.identifier = '007'
        self.solution = 'Ensure there are only one space between the "end" and "process" keywords.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isEndProcess:
                if not re.match('^\s*\S+\s\S', oLine.line):
                    self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'end')
