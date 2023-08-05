
from vsg.rules.signal import signal_rule
from vsg import fix
from vsg import check


class rule_004(signal_rule):
    '''
    Signal rule 004 checks the signal name is lowercase.
    '''

    def __init__(self):
        signal_rule.__init__(self)
        self.identifier = '004'
        self.solution = 'Change signal name to lowercase.'
        self.phase = 6

    def analyze(self, oFile):
        for iLineNumber, oLine in enumerate(oFile.lines):
            if oLine.isSignal:
                check.is_lowercase(self, oLine.line.split()[1], iLineNumber)

    def _fix_violations(self, oFile):
        for iLineNumber in self.violations:
            fix.lower_case(self, oFile.lines[iLineNumber], oFile.lines[iLineNumber].line.split()[1])
