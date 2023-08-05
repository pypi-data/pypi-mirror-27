from uuid import uuid4
import pytest


@pytest.mark.parametrize('failure_type', ['failure', 'error'])
@pytest.mark.parametrize('use_custom_message', [True, False])
def test_add_error_custom_exc_info(suite, suite_test, failure_type, use_custom_message):
    message = str(uuid4())

    if use_custom_message:
        add_error_args = '{!r}, '.format(message)
    else:
        add_error_args = ''

    add_error_args += 'exc_info=exc_info'

    code = """
import sys
try:
    1/0
except ZeroDivisionError:
    exc_info = sys.exc_info()
    try:
        None.a = 2
    except AttributeError:
        slash.add_{0}({1})
    """.format(failure_type, add_error_args)

    for line in code.strip().splitlines():
        suite_test.append_line(line)

    if failure_type == 'error':
        suite_test.expect_error()
    else:
        suite_test.expect_failure()
    summary = suite.run()
    [result] = summary.get_all_results_for_test(suite_test)

    if failure_type == 'error':
        [err] = result.get_errors()
    else:
        [err] = result.get_failures()

    assert err.has_custom_message() == use_custom_message
    if use_custom_message:
        assert err.message == message
    assert err.exception_type is ZeroDivisionError
    assert err.traceback.frames


def test_add_fatal_error(suite, suite_test):

    @suite_test.append_body
    def __code__():             # pylint: disable=unused-variable
        slash.add_error('bla').mark_fatal() # pylint: disable=undefined-variable

    suite_test.expect_error()
    for test in suite.iter_all_after(suite_test):
        test.expect_not_run()

    session = suite.run().session
    assert session.results.has_fatal_errors()


def test_session_level_add_error_message(suite, suite_test):
    @suite_test.file.append_body
    def __code__():                       # pylint: disable=unused-variable
        @slash.hooks.session_end.register # pylint: disable=undefined-variable
        def _callback():
            slash.add_error('session: add_error') # pylint: disable=undefined-variable
    res = suite.run(expect_session_errors=True)
    errors = res.session.results.global_result.get_errors()
    assert len(errors) == 1
    [err] = errors
    assert err.message == 'session: add_error'
