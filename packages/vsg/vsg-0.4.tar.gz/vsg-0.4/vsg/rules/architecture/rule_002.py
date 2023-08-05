
from vsg.rules.architecture import architecture_rule
from vsg import fix
from vsg import check

import re


class rule_002(architecture_rule):
    '''Architecture rule 002 checks for a single space between "architecture", "of", and "is" keywords.'''

    def __init__(self):
        architecture_rule.__init__(self)
        self.identifier = '002'
        self.solution = 'Remove extra spaces after architecture keyword.'
        self.phase = 2

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isArchitectureKeyword:
                if len(oLine.line.split()) > 4:
                    if not re.match('^\s*architecture\s\S+\sof\s\S+\sis', oLine.lineLower):
                        self.add_violation(iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'architecture')
            fix.enforce_one_space_before_word(self, oFile.lines[iLineNumber], 'of')
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'of')
            fix.enforce_one_space_before_word(self, oFile.lines[iLineNumber], 'is')
