import io
import os
import sys
import shutil as sh

MAGENTA = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
MUSTARD = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

FATAL_FILE = "./appgen-fatal.txt"


class Context:

    OPTS = {}

    @classmethod
    def get_opts(cls):
        return cls.OPTS

    @classmethod
    def read_opts(cls):
        # hack to make command line args position-independent
        # assumes any non '--' argument is the csv file, url, ...
        for idx, _ in enumerate(sys.argv):
            if idx == 0:
                continue
            elif sys.argv[idx].startswith("--"):
                cls.set_opt(sys.argv[idx], True)
            else:
                cls.ENTITY_ARG = sys.argv[idx]
        return len(sys.argv) > 1

    @classmethod
    def match_opt_prefix_or_default(cls, option_prefix, default=""):
        option = default
        for opt in Context.get_opts():
            if opt.startswith(option_prefix):
                option = opt.removeprefix(option_prefix)
        return option

    @classmethod
    def set_opt(cls, k, v):
        cls.OPTS[k] = v

    @classmethod
    def get_opt(cls, k):
        return cls.OPTS.get(k)

    @classmethod
    def has_opt(cls, stem):
        opt = cls.match_opt_prefix_or_default(stem)
        return opt != ""

    @staticmethod
    def banner(messages, color=MAGENTA):
        print(BOLD + color + ("=" * 120) + ENDC)
        for message in messages:
            print(BOLD + message + ENDC)
        print(BOLD + color + ("-" * 120) + ENDC)

    @classmethod
    def set_job(cls, job):
        if hasattr(cls, "JOB"):
            return
        cls.JOB = job

    @classmethod
    def _job_name(cls):
        if hasattr(cls, "JOB"):
            return cls.JOB
        return "None"

    @classmethod
    def _task_name(cls):
        if hasattr(cls, "CURRENT_TASK"):
            return cls.CURRENT_TASK.__name__
        return "None"

    @classmethod
    def _task_desc(cls):
        if hasattr(cls, "CURRENT_TASK"):
            return cls.CURRENT_TASK.description(cls)
        return "None"

    @classmethod
    def fatal(cls, message):
        if cls.get_opt("--quiet"):
            cls.banner([cls._job_name(), cls._task_name(), cls._task_desc()], color=RED)
        fatal_msg = BOLD + RED + "FATAL: " + ENDC + message
        cls.set_opt("--quiet", True)
        cls.append_data(FATAL_FILE, fatal_msg)
        cls.append_data(FATAL_FILE, f"JOB:  {cls._job_name()}")
        cls.append_data(FATAL_FILE, f"TASK: {cls._task_name()}")
        cls.append_data(FATAL_FILE, f"DESC: {cls._task_desc()}")
        cls.append_data(FATAL_FILE, cls)
        attrs = vars(cls)
        for item in attrs.items():
            cls.append_data(FATAL_FILE, item)
        print(fatal_msg)
        sys.exit(1)

    @classmethod
    def error(cls, message):
        if cls.get_opt("--quiet"):
            cls.banner([cls._job_name(), cls._task_name(), cls._task_desc()], color=RED)
        print(BOLD + RED + "ERROR: " + ENDC + message)

    @classmethod
    def warn(cls, message):
        if cls.get_opt("--quiet"):
            cls.banner(
                [cls._job_name(), cls._task_name(), cls._task_desc()], color=MUSTARD
            )
        print(BOLD + MUSTARD + "WARN: " + ENDC + message)

    @classmethod
    def info(cls, message):
        if cls.get_opt("--quiet"):
            return
        print(BOLD + BLUE + "INFO: " + ENDC + message)

    @classmethod
    def ok(cls, message):
        if cls.get_opt("--quiet"):
            return
        print(BOLD + GREEN + message + ENDC)

    USER_ACTIONS = []

    @classmethod
    def user_action(cls, action):
        cls.USER_ACTIONS.append(action)

    COMPLETED_TASKS = []

    @classmethod
    def completed(cls, action):
        cls.COMPLETED_TASKS.append(action)

    @classmethod
    def save_data(cls, filepath, data):
        msg = f"save: {filepath}"
        cls.info(msg)
        with open(filepath, "w", newline="\n") as file:
            file.write(data)

    @classmethod
    def save_data_and_verify(cls, filepath, data):
        msg = f"save/verify: {filepath}"
        cls.info(msg)
        cls.save_data(filepath, data)

        with open(filepath, "r") as file:
            saved_data = file.read()

        if data != saved_data:
            cls.fatal(f"save/verify file data mismatch in: {filepath}")

        msg = f"save/verify ok: {filepath}"
        cls.info(msg)

    @classmethod
    def append_data(cls, filepath, data):
        msg = f"append: {filepath}"
        cls.info(msg)
        with open(filepath, "a", newline="\n") as file:
            print(data, file=file)

    @classmethod
    def append_data_if_not_present(cls, filepath, data):
        with open(filepath, "r") as file:
            filedata = file.read()

        if data in filedata:
            cls.info(f"not appending to file: {filepath}")
            cls.info(f"content: {data}")
            return

        cls.append_data(filepath, data)

    @classmethod
    def copy_file(cls, filepath1, filepath2):
        msg = f"copy file: {filepath1} to {filepath2}"
        cls.info(msg)
        sh.copy(filepath1, filepath2)

    @classmethod
    def copy_folder(cls, filepath1, filepath2):
        msg = f"copy folder: {filepath1} to {filepath2}"
        cls.info(msg)
        sh.copytree(filepath1, filepath2)

    @classmethod
    def setx(cls, filepath):
        msg = f"setx: {filepath}"
        cls.info(msg)
        os.chmod(filepath, 0o744)

    @classmethod
    def exec(cls, task):
        if os.path.exists(FATAL_FILE):
            sys.exit(1)
        try:
            if hasattr(cls, "CURRENT_TASK"):
                cls.completed(cls._task_desc())
            cls.CURRENT_TASK = task
            if not cls.get_opt("--quiet"):
                cls.banner(
                    [
                        f"JOB:  {cls._job_name()}",
                        f"TASK: {cls._task_name()} - {cls._task_desc()}",
                    ]
                )
            task.exec(cls)
        except Exception as e:
            cls.fatal(f"{e}")

    @classmethod
    def ensure_folder(cls, folder):
        try:
            os.mkdir(folder)
            cls.info(f"folder: '{folder}' created successfully.")
        except FileExistsError:
            cls.info(f"folder: '{folder}' already exists.")
        except PermissionError:
            cls.fatal(f"no access to folder: '{folder}'.")
        except Exception as e:
            cls.fatal(f"{e}")

    @staticmethod
    def from_snake(name):
        class ret:
            ID = name + "_id"
            SNAKE_UCASE = name.upper()
            KEBAB = name.replace("_", "-")
            PASCAL_SPACED = name.replace("_", " ").title()
            PASCAL = PASCAL_SPACED.replace(" ", "")
            CAMEL = PASCAL[0].lower() + PASCAL[1:]
            LOWER_SPACED = name.replace("_", " ")
            PASCAL_SPACED_NO_ENUM = PASCAL_SPACED.removesuffix(" Enum")

        return ret

    @classmethod
    def hacky_get_ts_type_and_init_from_name(cls, name):
        if name.endswith("_enum"):
            return ("string", "''")
        if name.endswith("_id"):
            return ("number", -1)
        return ("string", "''")
