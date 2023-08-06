# system modules
import argparse
import logging
import textwrap
import itertools
import sys
import re
import os

# internal modules
from numericalmodel.utils import read_csv, write_csv
from numericalmodel.interfaces import *

# external modules
import IPython
import numpy as np


class NumericalModelArgumentParser(argparse.ArgumentParser):
    """
    An :any:`argparse.ArgumentParser` with predefined arguments useful for
    command-line interface of :any:`NumericalModel`.
    """

    def __init__(self, *args, **kwargs):
        instruction_parser = NumericalModelCliInstructionParser()
        parser_kwargs = {
            "description": "NumericalModel cli",
            "epilog": instruction_parser.INSTRUCTIONS_HELP,
            "formatter_class": argparse.RawDescriptionHelpFormatter
        }
        parser_kwargs.update(kwargs)

        super().__init__(*args, **parser_kwargs)

        self.add_argument("-v", "--verbose", help="run verbosely",
                          action="store_true")
        self.add_argument("-d", "-vv", "--debug", help="run with debug output",
                          action="store_true")
        self.add_argument("-i", "--input",
                          help="read instructions from file after processing "
                          "command-line arguments. Set to '-' for STDIN",
                          default=None,)

        self.add_argument("instructions", nargs="*",
                          help="Sequence of control statements.",
                          type=instruction_parser, default=[])


class NumericalModelCli(object):
    CLI_HELP = "To exit, type 'exit' or 'quit' or press CTRL-D."

    def __init__(self, model=None, argparser=None):
        self.model = model
        self.argparser = argparser

    @property
    def prompt(self):
        """
        The displayed prompt
        """
        return "{} >>>".format(self.model.name)

    @property
    def model(self):
        """
        The :any:`NumericalModel` behind the cli

        :type: :any:`NumericalModel`
        """
        try:
            return self._model
        except AttributeError:
            self._model = NumericalModel()
        return self._model

    @model.setter
    def model(self, newmodel):
        if newmodel is None:
            try:
                del self._model
            except AttributeError:
                pass
        else:
            assert all([hasattr(newmodel, a) for a in
                        ["integrate", "variables", "forcing", "parameters",
                         "observations"]])
            self._model = newmodel

    @property
    def argparser(self):
        """
        The :any:`argparse.ArgumentParser` to use for the cli

        :type: :any:`argparse.ArgumentParser`
        """
        try:
            return self._argparser
        except AttributeError:
            self._argparser = NumericalModelArgumentParser(
                description="command-line interface for {}"
                .format(self.model.name))
        return self._argparser

    @argparser.setter
    def argparser(self, newargparser):
        if newargparser is None:
            try:
                del self._argparser
            except AttributeError:
                pass
        else:
            assert all([hasattr(newargparser, a) for a in
                        ["parse_args", "instructions"]])
            self._argparser = newargparser

    @property
    def logger(self):
        """
        Logger
        """
        return logging.getLogger(self.__class__.__name__)

    @property
    def args(self):
        """
        The parsed arguments
        """
        try:
            return self._args
        except AttributeError:
            self._args = self.argparser.parse_args()
        return self._args

    @property
    def args_loglevel(self):
        """
        The loglevel to use, determined by :any:`args`
        """
        loglevel = logging.WARNING
        if self.args.verbose:
            loglevel = min(loglevel, logging.INFO)
        if self.args.debug:
            loglevel = min(loglevel, logging.DEBUG)
        return loglevel

    def execute_instructions(self, instructions=[]):
        """
        Execute given instructions

        Args:
            instructions (list, optional): The instructions to perform
        """
        def find_iv(ivid):
            iv = self.model.find(ivid)
            if not iv:
                self.logger.warning(
                    "name '{}' not found in model".format(ivid))
            return iv

        def all_ivids():
            res = []
            for a in \
                    ["variables", "parameters", "forcing", "observations"]:
                res.extend(getattr(self.model, a).keys())
            return res

        cp = NumericalModelCliInstructionParser
        for instruction in instructions:
            for action, p in instruction.items():
                self.logger.info("{} {}".format(self.prompt, p[cp.KW_CMD]))
                # variable assignment
                if action == cp.KW_ASSIGNMENT:
                    iv = find_iv(p[cp.KW_ID])  # find InterfaceValue
                    if iv:
                        self.logger.info("Setting '{}' to {} at " "time {}".format(
                            iv.id, p[cp.KW_VALUE], p[cp.KW_TIME]))
                        iv[p[cp.KW_TIME]] = p[cp.KW_VALUE]
                # integration
                elif action == cp.KW_INTEGRATE:
                    self.model.integrate(seconds=p[cp.KW_SECONDS])
                # file input
                elif action == cp.KW_FILEINPUT:
                    with open(p[cp.KW_FILE]) as f:
                        data = read_csv(f)
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else data.keys())}
                    # rename ids in file to ids in model
                    for id_in_file, id_in_model in p[cp.KW_TRANSLATION].items(
                    ):
                        try:
                            data[id_in_model] = data.pop(id_in_file)
                        except KeyError:
                            pass
                        try:
                            only[id_in_model] = only.pop(id_in_file)
                        except KeyError:
                            pass
                    if "time" in data:
                        for ivid, values in data.items():
                            if ivid == "time":
                                continue
                            if ivid in only:
                                iv = find_iv(ivid)
                                if not iv:
                                    continue
                                self.logger.info(
                                    "Setting {} to {} at times "
                                    "{}".format(
                                        ivid, values, data["time"]))
                                iv[:] = (data["time"], values)
                            else:
                                self.logger.info("Skipping '{}'".format(ivid))
                                continue
                    else:
                        self.logger.warning(
                            "File {} does not contain column "
                            "'time'. Skip import.".format(
                                p["file"]))
                # file output
                elif action == cp.KW_DUMP:
                    model_ivids = all_ivids()
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else model_ivids)}
                    ivs = {ivid: find_iv(ivid)
                           for ivid in only if find_iv(ivid)}
                    if ivs:
                        times = np.unique(np.concatenate(
                            [iv.times for ivid, iv in ivs.items()]))
                        # eliminate duplicates due to string conversion
                        times = np.array([float(x[0]) for x in
                                          itertools.groupby([str(i) for i in times])])
                        d = {ivid: iv(times).flatten()
                             for ivid, iv in ivs.items()}
                        d["time"] = times
                        for id_f, id_m in p[cp.KW_TRANSLATION].items():
                            try:
                                d[id_m] = d.pop(id_f)
                            except KeyError:
                                pass
                        with open(p[cp.KW_FILE], "w") as f:
                            self.logger.info("Writing {} to file '{}'..." .format(
                                list(d.keys()), p[cp.KW_FILE]))
                            write_csv(
                                f, d, headersortkey=lambda x: "" if x == "time" else x)
                # info
                elif action == cp.KW_CUT:
                    model_ivids = all_ivids()
                    only = {k: 1 for k in
                            (p[cp.KW_ONLY] if p[cp.KW_ONLY] else model_ivids)}
                    ivs = {ivid: find_iv(ivid)
                           for ivid in only if find_iv(ivid)}
                    start = p[cp.KW_SLICE][cp.KW_START]
                    end = p[cp.KW_SLICE][cp.KW_END]
                    for ivid, iv in ivs.items():
                        self.logger.info("Only keeping range [{}:{}] of '{}'"
                                         .format(start, end, ivid))
                        iv.cut(start, end)
                # info
                elif action == cp.KW_INFO:
                    iv = find_iv(p[cp.KW_ID])
                    print(repr(iv))
                # gui
                elif action == cp.KW_GUI:
                    self.model.gui(use_fallback=p[cp.KW_FALLBACK])
                # ipython
                elif action == cp.KW_IPYTHON:
                    m = self.model
                    model = self.model
                    IPython.embed(
                        header="Use variables 'm' or 'model' to access the model")
                # help
                elif action == cp.KW_HELP:
                    print("{}\n{}"
                          .format(self.CLI_HELP, cp.INSTRUCTIONS_HELP))
                # newobs
                elif action == cp.KW_NEWOBS:
                    iv = None
                    if p[cp.KW_FROM]:
                        self.logger.info("Copying '{}' to new observation "
                                         "'{}'".format(p[cp.KW_FROM], p[cp.KW_ID]))
                        old_iv = find_iv(p[cp.KW_FROM])
                        if old_iv:
                            iv = old_iv.copy(
                                id=p[cp.KW_ID],
                                name="[observation] {}".format(old_iv.name),
                                interpolation="linear")
                    if not iv:
                        self.logger.info("Creating new empty observation "
                                         "'{}'".format(p[cp.KW_ID]))
                        iv = InterfaceValue(
                            id=p[cp.KW_ID],
                            interpolation="linear",
                            name="observation")
                    self.model.observations.add_element(iv)
                # noop
                elif action == cp.KW_NOOP:
                    pass
                # optimization
                elif action == cp.KW_OPTIMIZE:
                    variate = {}
                    for ivid, nblocks in p[cp.KW_VARIATE].items():
                        iv = find_iv(ivid)
                        if iv:
                            variate.update({iv: int(nblocks)})
                    bring_together = []
                    for group in p[cp.KW_BRING_TOGETHER]:
                        l = []
                        for ivid in group:
                            l.append(find_iv(ivid))
                        bring_together.append(l)
                    # optimize
                    self.model.optimize(
                        bring_together=bring_together,
                        variate=variate,
                        time_start=p[cp.KW_SLICE][cp.KW_START],
                        time_end=p[cp.KW_SLICE][cp.KW_END],
                    )
                # exit
                elif action == cp.KW_EXIT:
                    sys.exit(0)

    def read_instructions(self, f=sys.stdin):
        """
        Read instructions from file

        Args:
            f (filehandle, optional): the file handle to read from
        """
        instruction_parser = NumericalModelCliInstructionParser()
        while True:
            sys.stdout.write("{} ".format(self.prompt))
            sys.stdout.flush()
            try:
                line = next(f)
                if not f.isatty():
                    sys.stdout.write(line)
                    sys.stdout.flush()
                if line.strip():
                    try:
                        self.execute_instructions(
                            [instruction_parser(line.strip())])
                    except argparse.ArgumentTypeError as e:
                        print(str(e))
            except StopIteration:
                break
            except KeyboardInterrupt:
                break

    def run(self, instructions=None):  # pragma: no cover
        """
        Run the command-line interface

        Args:
            instructions (list, optional): The instructions to perform
        """
        logging.basicConfig(level=self.args_loglevel)
        for n, l in logging.Logger.manager.loggerDict.items():
            l.level = self.args_loglevel

        self.logger.info("Model:\n{}".format(self.model))

        if instructions is None:
            instructions = self.args.instructions

        # execute command-line instructions
        self.execute_instructions(instructions)

        # read input file commands if desired
        f = None
        if self.args.input is not None:
            if self.args.input == '-':
                f = sys.stdin
            else:
                f = open(self.args.input, "r")
        elif not instructions:  # without arguments, drop into shell
            f = sys.stdin
        if f:
            self.read_instructions(f)


class NumericalModelCliInstructionParser(object):
    """
    Parser for instructions
    """
    # Keywords
    KW_ASSIGNMENT = "assign"
    KW_INTEGRATE = "integrate"
    KW_FILEINPUT = "fileinput"
    KW_FILE = "file"
    KW_GUI = "gui"
    KW_TIME = "time"
    KW_VALUE = "value"
    KW_ID = "id"
    KW_FALLBACK = "fallback"
    KW_DUMP = "dump"
    KW_SECONDS = "seconds"
    KW_INFO = "info"
    KW_KEYWORD = "keyword"
    KW_CMD = "cmd"
    KW_HELP = "help"
    KW_IPYTHON = "ipython"
    KW_EXIT = "exit"
    KW_OPTIMIZE = "optimize"
    KW_ONLY = "only"
    KW_TRANSLATION = "translation"
    KW_VARIATE = "variate"
    KW_BRING_TOGETHER = "bring_together"
    KW_NOOP = "noop"
    KW_NEWOBS = "newobs"
    KW_FROM = "from"
    KW_CUT = "cut"
    KW_SLICE = "slice"
    KW_START = "start"
    KW_END = "end"
    # Regexes
    REGEXES = {
        KW_ASSIGNMENT: re.compile(
            r"^(?P<{id}>\S+?)(?:\[(?P<{time}>\d+(?:\.\d+)?)\])?"
            "=(?P<{value}>\d+(?:\.\d+)?)$"
            .format(time=KW_TIME, id=KW_ID, value=KW_VALUE),
            flags=re.IGNORECASE),
        KW_INTEGRATE: re.compile(
            r"^(?P<{keyword}>int(?:egrate)?):(?P<{seconds}>\d+(?:\.\d+)?)$"
            .format(keyword=KW_KEYWORD, seconds=KW_SECONDS),
            flags=re.IGNORECASE),
        KW_INFO: re.compile(
            r"^(?P<{keyword}>info|show):(?P<{id}>\S+)$"
            .format(keyword=KW_KEYWORD, id=KW_ID),
            flags=re.IGNORECASE),
        KW_FILEINPUT: re.compile(
            r"^(?P<{keyword}>import|(?:file)?input|read(?:file)?):"
            r"(?P<{file}>\S+?)"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{trans}>\S+=\S+?(?:,\S+?=\S+?)*)\])?$"
            .format(keyword=KW_KEYWORD, only=KW_ONLY, trans=KW_TRANSLATION,
                    file=KW_FILE),
            flags=re.IGNORECASE),
        KW_CUT: re.compile(
            r"^(?P<{keyword}>cut)"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{slice}>\S*?:\S*?)\])?$"
            .format(keyword=KW_KEYWORD, only=KW_ONLY, slice=KW_SLICE),
            flags=re.IGNORECASE),
        KW_DUMP: re.compile(
            r"^(?P<{keyword}>dump|(?:file)?output|write(?:file)?):"
            r"(?P<{file}>\S+?)"
            r"(?:\[only:(?P<{only}>\S+?(,\S+?)*)\])?"
            r"(?:\[(?P<{trans}>\S+=\S+?(?:,\S+?=\S+?)*)\])?$"
            .format(keyword=KW_KEYWORD, only=KW_ONLY, trans=KW_TRANSLATION,
                    file=KW_FILE),
            flags=re.IGNORECASE),
        KW_GUI: re.compile(
            r"^(?P<{keyword}>gui)(?:\[(?P<{fallback}>fallback)\])?$"
            .format(keyword=KW_KEYWORD, fallback=KW_FALLBACK),
            flags=re.IGNORECASE),
        KW_HELP: re.compile(
            r"^(?P<{keyword}>(?:h(?:elp)?|\?))$"
            .format(keyword=KW_KEYWORD), flags=re.IGNORECASE),
        KW_NEWOBS: re.compile(
            r"^(?P<{keyword}>(?:new(?:obs(?:ervation)?)?)):(?P<{id}>\S+?)"
            r"(?:\[from:(?P<{fr}>\S+?)\])?$"
            .format(keyword=KW_KEYWORD, id=KW_ID, fr=KW_FROM),
            flags=re.IGNORECASE),
        KW_IPYTHON: re.compile(
            r"^(?P<{keyword}>(?:ipython|interactive|shell))$"
            .format(keyword=KW_KEYWORD), flags=re.IGNORECASE),
        KW_EXIT: re.compile(
            r"^(?P<{keyword}>(?:q(?:uit)?|exit))$"
            .format(keyword=KW_KEYWORD), flags=re.IGNORECASE),
        KW_OPTIMIZE: re.compile(
            r"^(?P<{keyword}>\S+)/"
            r"(?P<{bring_together}>\S+?=\S+(?:,\S+?=\S+?)*)/"
            r"(?P<{variate}>\S+?:\S+?(?:,\S+?:\S+?)*)"
            r"(?:\[(?P<{slice}>\S+?:\S+?)\])?$"
            .format(keyword=KW_KEYWORD, variate=KW_VARIATE,
                    bring_together=KW_BRING_TOGETHER, slice=KW_SLICE),
            flags=re.IGNORECASE),
        KW_NOOP: re.compile(r"^((\s*)|((#*\s*)*)|(\s*(#+\s*)+.*))$"),
    }
    # Examples
    INSTRUCTIONS_HELP = textwrap.dedent("""
        Example Instructions:

        Open GUI:

            "gui"

        Open GUI in fallback mode:

            "gui[fallback]"

        Integrate 60 seconds:

            "integrate:60"

        Set variable VARIABLE to value 64.1 at current time:

            "VARIABLE=64.1"

        Set variable VARIABLE to value 64.1 at time 42.5:

            "VARIABLE[42.5]=64.1"

        Read values from file DATA.csv:

            "input:DATA.csv" or
            "read:DATA.csv"

        Read only variables "T" and "f" from file DATA.csv:

            "read:DATA.csv[only:T,f]"

        Read variables "T" and "v" from file DATA.csv,
            but use them as "T_a" and "v_a" in the model:

            "read:DATA.csv[only:T,v][T=T_a,v=v_a]"

        Dump all data to file DATA.csv:

            "dump:DATA.csv"

        Dump variables "T" and "v" to file DATA.csv,
            but as "T_a" and "v_a" in the model:

            "dump:DATA.csv[only:T,v][T=T_a,v=v_a]"

        Create new observation "T_obs":

            "newobs:T_obs"

        Create new observation "T_obs" by copying "T_sim":

            "newobs:T_obs[from:T_sim]"

        Cut variable 'T_s' and only keep values between times 0 and 10:

            "cut[only:T_s][0:10]"

        Delete all values later than time 10:

            "cut[10:]"

        Optimize parameter "a" to match "T_sim" and "T_obs" best:

            "optimize/T_sim=T_obs/a:1"

        Optimize forcing "v" with 10 values to match "T_sim" and "T_obs" best
            in time range 0 to 20:

            "optimize/T_sim=T_obs/v:10[0:20]"

        Open an interactive IPython session to manipulate the model:

            "ipython" or
            "shell"
        """)

    def __call__(self, arg):
        """
        Parse an instruction string

        Args:
            arg (str): the string to parse

        Returns:
            dict : the parsed instruction
        """
        try:
            for keyword, regex in self.REGEXES.items():
                m = regex.match(arg)
                if m:
                    d = m.groupdict()
                    # post-processing
                    for k, v in d.items():
                        if k in [self.KW_SECONDS, self.KW_VALUE, self.KW_TIME]:
                            if v is not None:
                                d[k] = float(v)
                        if k in [self.KW_FALLBACK]:
                            d[k] = bool(v)
                        if k in [self.KW_TRANSLATION]:
                            d[k] = dict([p.split("=") for p in v.split(",")]) \
                                if v else {}
                        if k in [self.KW_BRING_TOGETHER]:
                            d[k] = [p.split("=") for p in v.split(",")] \
                                if v else []
                        if k in [self.KW_VARIATE]:
                            d[k] = dict([p.split(":") for p in v.split(",")]) \
                                if v else {}
                        if k in [self.KW_ONLY]:
                            d[k] = v.split(",") if v else []
                        if k in [self.KW_SLICE]:
                            s = {self.KW_START: None, self.KW_END: None}
                            if v:
                                for l, m in zip((self.KW_START, self.KW_END),
                                                v.split(":")):
                                    try:
                                        s[l] = float(m)
                                    except ValueError:
                                        s[l] = None
                            d[k] = s

                    d.update({self.KW_CMD: arg})
                    return {keyword: d}
                else:
                    continue
            # if we reach this point, this instruction is unknown
            assert False, "unknown instruction '{}'".format(arg)
        except (ValueError, AttributeError, AssertionError) as e:
            msg = "'{}' is no instruction: {}\n\n{}".format(
                arg, e, self.INSTRUCTIONS_HELP)
            raise argparse.ArgumentTypeError(msg)
