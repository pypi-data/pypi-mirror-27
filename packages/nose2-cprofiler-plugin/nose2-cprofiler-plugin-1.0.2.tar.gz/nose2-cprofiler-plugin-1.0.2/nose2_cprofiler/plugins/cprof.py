'''
Profile test execution using cProfile.
Config option ``sort`` can be used to change how profiling information
is presented.
'''
__all__ = ('Profiler',)

import logging
import cProfile
import pstats

import nose2

log = logging.getLogger('.'.join(('nose2', 'plugins', __package__)))


class Profiler(nose2.events.Plugin):

    """Profile the test run using cProfile"""

    configSection = 'profiler'
    commandLineSwitch = ('P', 'profile', 'Run test under cprofile')

    def __init__(self):
        self.sort = self.config.as_str('sort', 'cumulative')
        self.report_filename = self.config.as_str('filename', 'reports/profiler.prof')
        self.restrictions = (self.config.as_str('regex', []), self.config.as_int('count_of_lines_to_print', []))
        self.prof = None

    def startTestRun(self, event):
        """Setup profiler"""
        self.prof = cProfile.Profile()
        event.executeTests = self.prof.runcall

    def beforeSummaryReport(self, event):
        """Output profiling results"""
        self.prof.disable()
        stats = pstats.Stats(self.prof, stream=event.stream).sort_stats(
            self.sort)
        event.stream.writeln(nose2.util.ln('Profiling results'))
        stats.dump_stats(self.report_filename)
        stats.print_stats(*self.restrictions)
