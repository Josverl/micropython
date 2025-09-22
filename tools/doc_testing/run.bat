@echo off
REM Windows batch script for MicroPython documentation sample testing
REM This provides the same functionality as the Makefile echo   test-samples          - Test extracted code samples  
echo   test-samples-full     - Test with full analysis
echo   stats                 - Show statistics about extracted samples
echo   clean                 - Clean up generated files
echo   lint                  - Run linting with ruff
echo   format                - Format code with ruff
echo   check-format          - Check code formatting
echo   help                  - Show this help messageindows users

setlocal enabledelayedexpansion

set DOCS_PATH=..\..\docs
set OUTPUT_PATH=extracted_samples
set MICROPYTHON_STUBS_PATH=.\micropython-stubs
set PYTHON=python3

if "%1"=="" (
    echo MicroPython Documentation Sample Testing
    echo.
    echo Usage: %0 [command]
    echo.
    echo Commands:
    echo   setup                 - Set up the development environment
    echo   extract-samples       - Extract code samples from documentation
    echo   test-samples          - Test extracted code samples
    echo   test-samples-full     - Test with full analysis
    echo   stats                 - Show statistics about extracted samples
    echo   clean                 - Clean up generated files
    echo   lint                  - Run linting with ruff
    echo   format                - Format code with ruff
    echo   check-format          - Check code formatting
    echo   help                  - Show this help message
    goto :eof
)

if "%1"=="help" (
    goto :help
)

if "%1"=="setup" (
    echo Setting up development environment...
    %PYTHON% -m pip install --upgrade pip
    %PYTHON% -m pip install pytest pyyaml mypy astroid ruff
    
    if not exist "%MICROPYTHON_STUBS_PATH%" (
        echo Cloning micropython-stubs...
        git clone https://github.com/josverl/micropython-stubs.git %MICROPYTHON_STUBS_PATH%
        cd %MICROPYTHON_STUBS_PATH%
        if exist "pyproject.toml" (
            %PYTHON% -m pip install -e .
        ) else if exist "setup.py" (
            %PYTHON% -m pip install -e .
        )
        cd ..
    ) else (
        echo micropython-stubs already exists
    )
    echo Setup complete!
    goto :eof
)

if "%1"=="extract-samples" (
    echo Extracting code samples from %DOCS_PATH%...
    %PYTHON% extract_doc_samples.py %DOCS_PATH% --output %OUTPUT_PATH% --stats
    echo Extraction completed!
    goto :eof
)

if "%1"=="test-samples" (
    if not exist "%OUTPUT_PATH%" (
        echo No samples found, extracting first...
        call %0 extract-samples
    )
    echo Running basic tests on code samples...
    cd %OUTPUT_PATH%
    %PYTHON% -m pytest -v --tb=short --micropython-stubs-path=../%MICROPYTHON_STUBS_PATH% -p ../pytest_docsamples.py --disable-warnings .
    cd ..
    goto :eof
)

if "%1"=="test-samples-full" (
    if not exist "%OUTPUT_PATH%" (
        echo No samples found, extracting first...
        call %0 extract-samples
    )
    echo Running full analysis on code samples...
    cd %OUTPUT_PATH%
    %PYTHON% -m pytest -v --tb=short --micropython-stubs-path=../%MICROPYTHON_STUBS_PATH% -p ../pytest_docsamples.py --run-static-analysis --run-execution-test --disable-warnings .
    cd ..
    goto :eof
)

if "%1"=="stats" (
    if exist "%OUTPUT_PATH%" (
        echo Sample Statistics:
        for /f %%i in ('%PYTHON% -c "import pathlib; print(len(list(pathlib.Path('%OUTPUT_PATH%').glob('*.py'))))"') do echo Total samples: %%i
        echo.
        echo By platform:
        %PYTHON% -c "import pathlib; samples = list(pathlib.Path('%OUTPUT_PATH%').glob('*.py')); platforms = {}; [platforms.setdefault(p.name.split('_')[0], 0) or platforms.update({p.name.split('_')[0]: platforms[p.name.split('_')[0]] + 1}) for p in samples if '_' in p.name]; [print(f'  {k}: {v}') for k, v in sorted(platforms.items()) if v > 0]"
    ) else (
        echo No samples directory found. Run '%0 extract-samples' first.
    )
    goto :eof
)

if "%1"=="clean" (
    echo Cleaning up generated files...
    if exist "%OUTPUT_PATH%" rmdir /s /q "%OUTPUT_PATH%"
    for /d /r . %%d in (__pycache__) do if exist "%%d" rd /s /q "%%d" 2>nul
    del /s /q *.pyc 2>nul
    echo Cleanup complete
    goto :eof
)

if "%1"=="lint" (
    echo Running linting with ruff...
    %PYTHON% -m ruff check .
    %PYTHON% -m mypy . --ignore-missing-imports
    goto :eof
)

if "%1"=="format" (
    echo Formatting code with ruff...
    %PYTHON% -m ruff format .
    goto :eof
)

if "%1"=="check-format" (
    echo Checking code formatting with ruff...
    %PYTHON% -m ruff format --check .
    goto :eof
)

echo Unknown command: %1
echo Run '%0 help' for available commands.

:help
echo MicroPython Documentation Sample Testing
echo.
echo Usage: %0 [command]
echo.
echo Commands:
echo   setup                 - Set up the development environment
echo   extract-samples       - Extract code samples from documentation  
echo   test-samples          - Test extracted code samples
echo   test-samples-full     - Test with full analysis
echo   stats                 - Show statistics about extracted samples
echo   clean                 - Clean up generated files
echo   help                  - Show this help message
echo.
echo Configuration:
echo   DOCS_PATH=%DOCS_PATH%
echo   OUTPUT_PATH=%OUTPUT_PATH%
echo   MICROPYTHON_STUBS_PATH=%MICROPYTHON_STUBS_PATH%