
from vsg.rules.process import process_rule
from vsg import utilities
from vsg import fix
from vsg import check


class rule_008(process_rule):
    '''
    Process rule 008 checks the "end" keyword is lowercase.
    '''

    def __init__(self):
        process_rule.__init__(self)
        self.identifier = '008'
        self.solution = 'Lowercase the "end" keyword.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isEndProcess:
                check.is_lowercase(self, utilities.get_first_word(oLine), iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.lower_case(self, oFile.lines[iLineNumber], 'end')
