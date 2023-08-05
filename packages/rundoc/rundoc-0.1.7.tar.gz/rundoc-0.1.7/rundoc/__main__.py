"""
Main module for rundoc command line utility.
"""
from bs4 import BeautifulSoup
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_pygments
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_by_name
from pygments.styles.tango import TangoStyle
from pygments.styles.vim import VimStyle
from time import sleep
import argcomplete
import argparse
import json
import logging
import markdown
import os
import re
import rundoc
import signal
import subprocess
import sys

class clr:
    ''' 
    ANSI colors for pretty output.
    '''
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class DocCode(object):
    """Single multi-line code block executed as a script.

    Attributes:
        interpreter (str): Interpreter used to run the code.
        code (str): Base code loaded during initialization.
        user_code (str): User modified version of the code (will be used
            instead if is not None or empty string).
        process (subprocess.Popen): Process object running the interpreter.
        output (dict): Dictinary containing 'stdout' and 'retcode'.
    """
    def __init__(self, code, interpreter):
        self.interpreter = interpreter
        self.code = code
        self.user_code = ''
        self.process = None
        self.output = { 'stdout':'', 'retcode':None }

    def get_lexer_class(self):
        lexer_class = None
        try:
            # try because lexer may not exist for current interpreter
            return get_lexer_by_name(self.interpreter).__class__
        except:
            # no lexer, return plain text
            return None

    def __str__(self):
        lexer_class = self.get_lexer_class()
        code = self.user_code.strip() or self.code
        if lexer_class:
            return highlight(
                code,
                lexer_class(),
                Terminal256Formatter(style=VimStyle)
                )
        return code

    def get_dict(self):
        return {
            'interpreter': self.interpreter,
            'code': self.code,
            'user_code': self.user_code,
            'output': self.output,
        }

    def prompt_user(self, prompt_text=' '):
        self.user_code = prompt(
            prompt_text,
            default = self.code,
            lexer = self.get_lexer_class(),
            style = style_from_pygments(VimStyle)
            )

    def print_stdout(self):
        assert self.process
        line = self.process.stdout.readline().decode('utf-8')
        self.output['stdout'] += line
        print(line, end='')

    def is_running(self):
        return self.process and self.process.poll() is None

    def run(self):
        if not self.process:
            code = self.user_code.strip() or self.code
            logging.debug('Running code {}'.format(code))
            self.process = subprocess.Popen(
                [self.interpreter, '-c', code],
                stdout=subprocess.PIPE,
                stderr=sys.stdout.buffer,
                shell=False,
                )
        while self.is_running():
            self.print_stdout()
        self.output['retcode'] = self.process.poll()

    def kill(self):
        if self.process:
             self.process.kill()


class DocCommander(object):
    """
    Manages environment and DocCode objects and executes them in succession.
    """
    def __init__(self):
        self.env = {}
        self.env_lines = []
        self.doc_codes = []
        self.running = False
        self.failed = False
        self.current_doc_code = None
        signal.signal(signal.SIGINT, self.__signal_handler)

    def __signal_handler(self, signal, frame):
        """Handle keyboard interrupt."""
        logging.debug('KeyboardInterrupt received.')
        sys.stderr.write(
            "\nKeyboardInterrupt captured. Stopping rundoc gracefully.\n")
        if self.current_doc_code:
            self.current_doc_code.kill()
        else:
            sys.exit(1)

    def get_dict(self):
        return [ x.get_dict() for x in self.doc_codes ]

    def add(self, code, interpreter='bash'):
        if not interpreter:
            interpreter = 'bash'
        self.doc_codes.append(DocCode(code, interpreter))

    def set_env(self, env_string):
        for line in env_string.strip().split('\n'):
            if not line: continue
            if '=' not in line:
                logging.error('{}\n^ Bad environment entry.'.format(line))
                sys.exit(0)
            var, value = line.split('=', 1)
            var = var.strip()
            value = value.strip()
            if not var: continue
            self.env_lines.append((var, value))

    def __load_env(self, yes=False):
        if len(self.env_lines) and not yes:
            msg = "\n{}═══╣ Confirm/supply/modify environment variables:{}"
            msg = msg.format(clr.BOLD, clr.END)
            print(msg)
        for var, value in self.env_lines:
            user_env = value or os.environ.get(var, '')
            if not yes or not user_env:
                user_env = input('{}={}  '.format(var, user_env)) or user_env
            os.environ[var] = user_env

    def run(self, step=1, yes=False, pause=0):
        """Run all the doc_codes one by one starting from `step`.

        Args:
            step (int): Number of step to start with. Defaults to 1. Steps
                start at 1.
            yes (bool): Auto-confirm all steps without user interaction.
                Defaults to False.

        Returns:
            JSON representation of commands and outputs.
        """
        logging.debug('Running DocCommander.')
        assert self.running == False
        assert self.failed == False
        self.__load_env(yes=yes)
        self.running = True
        for doc_code in self.doc_codes[step-1:]:
            logging.debug("Beginning of step {}".format(step))
            prompt_text = "\n{}=== Step {} [{}]{}".format(
                clr.BOLD,
                step,
                doc_code.interpreter,
                clr.END,
                )
            print(prompt_text)
            if yes:
                print(doc_code)
                sleep(pause)
            else:
                doc_code.prompt_user()
            self.current_doc_code = doc_code
            self.current_doc_code.run() # run in blocking manner
            if doc_code.output['retcode'] == 0:
                logging.debug("Step {} finished.".format(step))
            else:
                self.failed = True
            if self.failed:
                self.running = False
                logging.error('Failed on step {}'.format(step))
                print("==== {}Failed at step {} with exit code '{}'{}\n".format(
                    clr.RED,
                    step,
                    doc_code.output['retcode'],
                    clr.END,
                    )
                )
                self.current_doc_code = None
                break
            self.current_doc_code = None
            print("{}==== Step {} done{}\n".format(clr.GREEN, step, clr.END))
            step += 1
        return json.dumps(self.get_dict(), sort_keys=True, indent=4)

def __parse_args():
    """Parse command line arguments and return an argparse object."""
    parser = argparse.ArgumentParser(
        prog = "rundoc",
        description="Run code from markdown code blocks in controlled manner",
        )
    parser.add_argument(
        "-v", "--version", action="store_true",
        help="Show version info and exit."
        )
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="Enable debug mode with output of each action in the log."
        )
    subparsers = parser.add_subparsers(
        description="(use each command with -h for more help)",
        dest="cmd",
        )

    parser_run = subparsers.add_parser(
        "run",
        description="Run markdown as a script."
        )
    parser_run.add_argument(
        "mkd_file_path", type=str, action="store",
        help="Markdown file path."
        )
    parser_run.add_argument(
        "-t", "--tags", action="store",
        help='''Coma-separated list of tags (e.g. -t
            bash,bash_proj-2,python3_proj2). Part of tag until first underscore
            will be used as selected interpreter for that code. If no tags are
            provided, all code blocks will be used. Untagged code blocks will
            use bash as default interpreter.'''
        )
    parser_run.add_argument(
        "-p", "--pause", type=int, action="store",
        help='''Used in combination with -y. Pause N seconds before each code
                block. Defaults to 0.'''
        )
    parser_run.add_argument(
        "-s", "--step", type=int, action="store",
        help="Start at step STEP. Defaults to 1."
        )
    parser_run.add_argument(
        "-o", "--output", type=str, action="store",
        help='''Output file. All codes, modifications and output of execution
            will be saved here. This file can be later used as an argument to
            'rerun' command which will execute all steps without any user
            interaction.'''
        )
    parser_run.add_argument(
        "-y", "--yes", action="store_true",
        help="Confirm all steps with no user interaction."
        )
    parser_run.set_defaults(
        tags="",
        pause=0,
        step=1,
        output=None,
        )

    parser_rerun = subparsers.add_parser(
        "rerun",
        description="Run codes saved as json output by 'run' command."
        )
    parser_rerun.add_argument(
        "saved_output_path", type=str, action="store",
        help="Path of saved output file from 'run' or 'rerun' command."
        )
    parser_rerun.add_argument(
        "-s", "--step", type=int, action="store",
        help="Start at step STEP. Defaults to 1."
        )
    parser_rerun.add_argument(
        "-o", "--output", type=str, action="store",
        help='''Output file. All codes, modifications and output of execution
            will be saved here. This file can be later used as an input
            argument to 'rerun' command.'''
        )
    parser_rerun.set_defaults(
        step=1,
        output=None,
        )

    argcomplete.autocomplete(parser)
    return parser.parse_args()

def parse_doc(mkd_file_path, tags=""):
    """Parse code blocks from markdown file and return DocCommander object.

    Args:
        mkd_file_path (str): Path to markdown file.
        code_tag (str): Code highlight specifier in markdown. We can use this
            to filter only certain code blocks. If it's set to empty string or
            None, all code blocks will be used. Defaults to "bash".

    Returns:
        DocCommander object.
    """
    mkd_data = ""
    with open(mkd_file_path, 'r') as f:
        mkd_data = f.read()
    html_data = markdown.markdown(
        mkd_data,
        extensions=['toc', 'tables', 'footnotes', 'fenced_code']
        )
    soup = BeautifulSoup(html_data, 'html.parser')
    # collect all elements with selected tags as classes
    classes = re.compile(
        "(^|_)({})(_|$)".format('|'.join(tags.split(','))) if tags else '^(?!env).*'
        )
    code_block_elements = soup.findAll('code', attrs={"class":classes,})
    commander = DocCommander()
    for element in code_block_elements:
        class_name = element.get_attribute_list('class')[0]
        interpreter = None
        if class_name:
            interpreter = class_name.split("_")[0]
        commander.add(
            element.getText(),
            interpreter
        )
    classes = re.compile("^env(iron(ment)?)?$")
    env_elements = soup.findAll('code', attrs={"class":classes,})
    env_string = "\n".join([ x.string for x in env_elements ])
    commander.set_env(env_string)
    return commander

def parse_output(output_file_path):
    """Load json output, create and return DocCommander object.

    Args:
        output_file_path (str): Path to saved output file.

    Returns:
        DocCommander object.
    """
    output_data = None
    with open(output_file_path, 'r') as f:
        output_data = f.read()
    data = json.loads(output_data)
    commander = DocCommander()
    for d in data:
        doc_code = DocCode(d['code'], d['interpreter'])
        doc_code.user_command = d['user_code']
        commander.doc_codes.append(doc_code)
    return commander


def main():
    args = __parse_args()
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)03d, %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = None,
        level = logging.DEBUG if args.debug else logging.CRITICAL,
        )
    if args.version:
        print("rundoc {} - Copyright {} {} <{}>".format(
            rundoc.__version__,
            rundoc.__year__,
            rundoc.__author__,
            rundoc.__author_email__,
            ))
        sys.exit(0)
    output = ""
    if args.cmd == 'run':
        commander = parse_doc(args.mkd_file_path, tags=args.tags)
        output = commander.run(step=args.step, yes=args.yes, pause=args.pause)
    if args.cmd == 'rerun':
        commander = parse_output(args.saved_output_path)
        output = commander.run(step=args.step, yes=True)
    if args.cmd in ('rerun', 'run') and args.output:
        with open(args.output, 'w+') as f:
            f.write(output)

if __name__ == '__main__':
    main()

