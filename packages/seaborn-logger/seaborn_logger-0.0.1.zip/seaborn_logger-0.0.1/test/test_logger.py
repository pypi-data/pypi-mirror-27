from seaborn.logger import *

def smoke_test():
    import requests
    log_file = os.path.join(os.path.split(__file__)[0], '_test.log')
    SeabornFormatter(relative_pathname="/seaborn/seaborn/").setup_logging(log_filename=log_file,
                                                                          silence_modules=['requests'],
                                                                          log_level='TRACE',
                                                                          log_stdout_level='TRACE')
    msg = "Test: Hello World (Logger Worked)"
    log.trace(msg)
    test_exclusion = requests.get('http://google.com')
    logged_message = open(log_file, 'r').read()
    assert logged_message.strip().endswith(msg), 'Bad Log Message: %s' % logged_message


if __name__ == '__main__':
    smoke_test()
