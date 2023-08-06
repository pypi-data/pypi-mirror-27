import tempfile
import webbrowser
import os
import __main__

def browser_preview(string_content, dir=None):
    """ Creates a temporary html file with the string_content, and opens it in a browser
    The script then waits for user input and when entered cleans up the temporary file

    set dir=False to use system default location for temporary file.
        dir=None puts file in current directory, to allow relative links to work in testing
    """
    with tempfile.NamedTemporaryFile(suffix='.html',
                                     delete=True,
                                     dir=os.path.dirname(__main__.__file__) if dir is None
                                     else (None if dir is False else dir)) as file:
        file.write(str(string_content).encode('utf-8'))
        file.flush()
        print(r'file:\\' + file.name)
        webbrowser.open(r'file:///' + file.name.replace('\\', '/'))
        input("Press Enter to end script and clean up temporary file...")
