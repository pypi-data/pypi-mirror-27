from __future__ import unicode_literals

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.contrib.completers import PathCompleter
from prompt_toolkit.contrib.regular_languages.compiler import compile as compile_grammar
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter

from rp.rp_ptpython.utils import get_jedi_script_from_document

import re

__all__ = (
    'PythonCompleter',
)

class PathCompleter(Completer):
    """
    Complete for Path variables.

    :param get_paths: Callable which returns a list of directories to look into
                      when the user enters a relative path.
    :param file_filter: Callable which takes a filename and returns whether
                        this file should show up in the completion. ``None``
                        when no filtering has to be done.
    :param min_input_len: Don't do autocompletion when the input string is shorter.
    """
    def __init__(self, only_directories=False, get_paths=None, file_filter=None,
            min_input_len=0, expanduser=False):
        assert get_paths is None or callable(get_paths)
        assert file_filter is None or callable(file_filter)
        assert isinstance(min_input_len, int)
        assert isinstance(expanduser, bool)

        self.only_directories = only_directories
        self.get_paths = get_paths or (lambda: ['.'])
        self.file_filter = file_filter or (lambda _: True)
        self.min_input_len = min_input_len
        self.expanduser = expanduser

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # Complete only when we have at least the minimal input length,
        # otherwise, we can too many results and autocompletion will become too
        # heavy.
        if len(text) < self.min_input_len:
            return

        try:
            # Do tilde expansion.
            if self.expanduser:
                text = os.path.expanduser(text)

            # Directories where to look.
            dirname = os.path.dirname(text)
            if dirname:
                directories = [os.path.dirname(os.path.join(p, text))
                               for p in self.get_paths()]
            else:
                directories = self.get_paths()

            # Start of current file.
            prefix = os.path.basename(text)

            # Get all filenames.
            filenames = []
            for directory in directories:
                # Look for matches in this directory.
                if os.path.isdir(directory):
                    for filename in os.listdir(directory):
                        if filename.startswith(prefix):
                            filenames.append((directory, filename))

            # Sort
            filenames = sorted(filenames, key=lambda k: k[1])

            # Yield them.
            for directory, filename in filenames:
                completion = filename[len(prefix):]
                full_name = os.path.join(directory, filename)

                if os.path.isdir(full_name):
                    # For directories, add a slash to the filename.
                    # (We don't add them to the `completion`. Users can type it
                    # to trigger the autocompletion themself.)
                    filename += '/'
                elif self.only_directories:
                    continue

                if not self.file_filter(full_name):
                    continue

                yield Completion(completion, 0, display=filename)
        except OSError:
            pass
class PythonCompleter(Completer):
    """
    Completer for Python code.
    """
    def __init__(self, get_globals, get_locals):
        super(PythonCompleter, self).__init__()

        self.get_globals = get_globals
        self.get_locals = get_locals

        self._path_completer_cache = None
        self._path_completer_grammar_cache = None

    @property
    def _path_completer(self):
        if self._path_completer_cache is None:
            self._path_completer_cache = GrammarCompleter(
                self._path_completer_grammar, {
                    'var1': PathCompleter(expanduser=True),
                    'var2': PathCompleter(expanduser=True),
                })
        return self._path_completer_cache

    @property
    def _path_completer_grammar(self):
        """
        Return the grammar for matching paths inside strings inside Python
        code.
        """
        # We make this lazy, because it delays startup time a little bit.
        # This way, the grammar is build during the first completion.
        if self._path_completer_grammar_cache is None:
            self._path_completer_grammar_cache = self._create_path_completer_grammar()
        return self._path_completer_grammar_cache

    def _create_path_completer_grammar(self):
        def unwrapper(text):
            return re.sub(r'\\(.)', r'\1', text)

        def single_quoted_wrapper(text):
            return text.replace('\\', '\\\\').replace("'", "\\'")

        def double_quoted_wrapper(text):
            return text.replace('\\', '\\\\').replace('"', '\\"')

        grammar = r"""
                # Text before the current string.
                (
                    [^'"#]                                  |  # Not quoted characters.
                    '''  ([^'\\]|'(?!')|''(?!')|\\.])*  ''' |  # Inside single quoted triple strings
                    "" " ([^"\\]|"(?!")|""(?!^)|\\.])* "" " |  # Inside double quoted triple strings

                    \#[^\n]*(\n|$)           |  # Comment.
                    "(?!"") ([^"\\]|\\.)*"   |  # Inside double quoted strings.
                    '(?!'') ([^'\\]|\\.)*'      # Inside single quoted strings.

                        # Warning: The negative lookahead in the above two
                        #          statements is important. If we drop that,
                        #          then the regex will try to interpret every
                        #          triple quoted string also as a single quoted
                        #          string, making this exponentially expensive to
                        #          execute!
                )*
                # The current string that we're completing.
                (
                    ' (?P<var1>([^\n'\\]|\\.)*) |  # Inside a single quoted string.
                    " (?P<var2>([^\n"\\]|\\.)*)    # Inside a double quoted string.
                )
        """

        return compile_grammar(
            grammar,
            escape_funcs={
                'var1': single_quoted_wrapper,
                'var2': double_quoted_wrapper,
            },
            unescape_funcs={
                'var1': unwrapper,
                'var2': unwrapper,
            })

    def _complete_path_while_typing(self, document):
        char_before_cursor = document.char_before_cursor
        return document.text and (
            char_before_cursor.isalnum() or char_before_cursor in '/.~')

    def _complete_python_while_typing(self, document):
        char_before_cursor = document.char_before_cursor
        return document.text and (
            char_before_cursor.isalnum() or char_before_cursor in '_.')

    def get_completions(self, document, complete_event):
        """
        Get Python completions.
        """
        # Do Path completions
        if complete_event.completion_requested or self._complete_path_while_typing(document):
            for c in self._path_completer.get_completions(document, complete_event):
                yield c

        # If we are inside a string, Don't do Jedi completion.
        if self._path_completer_grammar.match(document.text_before_cursor):
            return

        # Do Jedi Python completions.
        if complete_event.completion_requested or self._complete_python_while_typing(document):
            script = get_jedi_script_from_document(document, self.get_locals(), self.get_globals())

            if script:
                try:
                    completions = script.completions()
                except TypeError:
                    # Issue #9: bad syntax causes completions() to fail in jedi.
                    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/9
                    pass
                except UnicodeDecodeError:
                    # Issue #43: UnicodeDecodeError on OpenBSD
                    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/43
                    pass
                except AttributeError:
                    # Jedi issue #513: https://github.com/davidhalter/jedi/issues/513
                    pass
                except ValueError:
                    # Jedi issue: "ValueError: invalid \x escape"
                    pass
                except KeyError:
                    # Jedi issue: "KeyError: u'a_lambda'."
                    # https://github.com/jonathanslenders/ptpython/issues/89
                    pass
                except IOError:
                    # Jedi issue: "IOError: No such file or directory."
                    # https://github.com/jonathanslenders/ptpython/issues/71
                    pass
                except AssertionError:
                    # In jedi.parser.__init__.py: 227, in remove_last_newline,
                    # the assertion "newline.value.endswith('\n')" can fail.
                    pass
                except SystemError:
                    # File "jedi/api/helpers.py", line 140, in get_stack_at_position
                    # raise SystemError("This really shouldn't happen. There's a bug in Jedi.")
                    pass
                else:
                    for c in completions:
                        yield Completion(c.name_with_symbols, len(c.complete) - len(c.name_with_symbols),
                                         display=c.name_with_symbols)
