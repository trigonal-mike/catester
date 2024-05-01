#https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
def get_pytest_flags(
        reportPassed: bool = True,
        withHeader: bool = True,
        withSummary: bool = True,
        withTraceback: bool = True,
        fullTraceback: bool = False,
        collectOnly: bool = False,
        showFixtures: bool = False,
        showLocals: bool = False,
        exitOnFirstError: bool = False,
        verbosity: int = 0,
    ):
    flags = [f"--verbosity={verbosity}"]
    if reportPassed:
        flags.append("-rA")
    else:
        flags.append("-ra")
    if not withHeader:
        flags.append("--no-header")
    if not withSummary:
        flags.append("--no-summary")
    if not withTraceback:
        flags.append("--tb=no")
    else:
        flags.append("--tb=line")
    if fullTraceback:
        flags.append("--full-trace")
    if collectOnly:
        flags.append("--collect-only")
    if showFixtures:
        flags.append("--fixtures")
    if showLocals:
        flags.append("--showlocals")
    if exitOnFirstError:
        flags.append("-x")

    return ",".join(flags)
