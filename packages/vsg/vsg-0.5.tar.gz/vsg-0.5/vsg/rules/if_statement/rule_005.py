
from vsg import rule
from vsg import fix

import re


class rule_005(rule.rule):
    '''If rule 005 checks there is a single space between the "elsif" keyword and the (.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'if'
        self.identifier = '005'
        self.solution = 'Ensure only a single space exists between the "elsif" keyword and the (.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isElseIfKeyword:
                if re.match('^\s*elsif\s*\(', oLine.lineLower):
                    if not re.match('^\s*elsif\s\(', oLine.lineLower):
                        self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'elsif')
