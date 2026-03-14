import io
import os
import re
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

FATAL_FILE = "./fatal.txt"

# add the common domain
app_dir = f'{os.environ["__APPGEN_CMD_PATH__"]}'
sys.path.append(app_dir)

# add the implementation domains
db_dir = f'{os.environ["__APPGEN_DB_PATH__"]}'
sys.path.append(db_dir)
api_dir = f'{os.environ["__APPGEN_API_PATH__"]}'
sys.path.append(api_dir)
fe_dir = f'{os.environ["__APPGEN_FE_PATH__"]}'
sys.path.append(fe_dir)


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
        cls.exit_if_fatal()

        if hasattr(cls, "JOB"):
            return
        cls.JOB = job

        cls.APP_APP_PATH = "./"

        cls.APP_BACKEND_PATH = cls.match_opt_prefix_or_default(
            "--backend-path=", "./backend"
        )
        cls.ensure_folder(cls.APP_BACKEND_PATH)
        cls.APP_DATABASE_PATH = f"{cls.APP_BACKEND_PATH}/database"
        cls.ensure_folder(cls.APP_DATABASE_PATH)
        cls.APP_API_PATH = f"{cls.APP_BACKEND_PATH}/api"
        cls.ensure_folder(cls.APP_API_PATH)
        cls.APP_FRONTEND_PATH = cls.match_opt_prefix_or_default(
            "--frontend-path=", "./frontend"
        )
        cls.ensure_folder(cls.APP_FRONTEND_PATH)

        # template paths - relative to appgen, set from environment
        cls.COMPONENTS_APP_PATH = f'{os.environ["__APPGEN_CMD_PATH__"]}/components'
        cls.COMPONENTS_DB_PATH = f'{os.environ["__APPGEN_DB_PATH__"]}/components'
        cls.COMPONENTS_UI_PATH = f'{os.environ["__APPGEN_FE_PATH__"]}/components'
        cls.COMPONENTS_API_PATH = f'{os.environ["__APPGEN_API_PATH__"]}/components'

        # application folder structure - relative to current directory
        cls.CONFIGURE_PATH = cls.match_opt_prefix_or_default(
            "--configure-path=", "./configure"
        )
        cls.ensure_folder(cls.CONFIGURE_PATH)
        cls.CSV_SCHEMA_PATH = f"{cls.CONFIGURE_PATH}/schema_csv"
        cls.ensure_folder(cls.CSV_SCHEMA_PATH)
        cls.JSON_SCHEMA_PATH = f"{cls.CONFIGURE_PATH}/schema_json"
        cls.ensure_folder(cls.JSON_SCHEMA_PATH)

        # hack to support no schema, this belongs in the DB context
        # target paths
        cls.APP_DATABASE_SCRIPTS_PATH = f"{cls.APP_DATABASE_PATH}/scripts"
        cls.ensure_folder(cls.APP_DATABASE_SCRIPTS_PATH)

        cls.APP_DATABASE_CSV_SEED_PATH = f"{cls.APP_DATABASE_PATH}/csv_seed"
        cls.ensure_folder(cls.APP_DATABASE_CSV_SEED_PATH)

        cls.APP_DATABASE_SQL_PATH = f"{cls.APP_DATABASE_PATH}/sql"
        cls.ensure_folder(cls.APP_DATABASE_SQL_PATH)

        cls.ENTITY_FIELDS_STEM = "--entity-fields="

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
    def exit_if_fatal(cls):
        if os.path.exists(FATAL_FILE):
            cls.banner([f"ABORTING: file {FATAL_FILE} was detected"], color=RED)
            sys.exit(1)

    @classmethod
    def exec(cls, task):
        cls.exit_if_fatal()
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

    @classmethod
    def ensure_folders(cls, folders):
        try:
            os.makedirs(folders)
            cls.info(f"folders: '{folders}' created successfully.")
        except FileExistsError:
            cls.info(f"folders: '{folders}' already exists.")
        except PermissionError:
            cls.fatal(f"no access to folders: '{folders}'.")
        except Exception as e:
            cls.fatal(f"{e}")

    @staticmethod
    def pascal_spaced_from_pascal(name):
        # return " ".join(re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))
        return " ".join(re.findall(r"[A-Z][^A-Z]*", name))

    @staticmethod
    def pascal_from_snake(name):
        pascal_spaced = name.replace("_", " ").title()
        return pascal_spaced.replace(" ", "")

    @classmethod
    def generate_entity_names_from_pascal(cls, pascal):
        class ret:
            PASCAL = pascal  # assume PascalCase
            PASCAL_SPACED = cls.pascal_spaced_from_pascal(PASCAL)
            LOWER_SPACED = PASCAL_SPACED.lower()
            SNAKE = LOWER_SPACED.replace(" ", "_")
            ID = SNAKE + "_id"
            SNAKE_UCASE = SNAKE.upper()
            KEBAB = SNAKE.replace("_", "-")
            CAMEL = PASCAL[0].lower() + PASCAL[1:]
            PASCAL_SPACED_NO_ENUM = PASCAL_SPACED.removesuffix(" Enum")

        return ret

    @classmethod
    def generate_entity_names_from_snake(cls, snake):
        pascal_spaced = snake.replace("_", " ").title()
        pascal = pascal_spaced.replace(" ", "")
        return cls.generate_entity_names_from_pascal(pascal)

    @classmethod
    def set_entity_names_from_pascal(cls, pascal):
        names = cls.generate_entity_names_from_pascal(pascal)
        cls.ENTITY_PASCAL = names.PASCAL
        cls.ENTITY_PASCAL_SPACED = names.PASCAL_SPACED
        cls.ENTITY_SNAKE = names.SNAKE
        cls.ENTITY_ID = names.ID
        cls.ENTITY_SNAKE_UCASE = names.SNAKE_UCASE
        cls.ENTITY_KEBAB = names.KEBAB
        cls.ENTITY_CAMEL = names.CAMEL
        cls.ENTITY_LOWER_SPACED = names.LOWER_SPACED
        cls.ENTITY_PASCAL_SPACED_NO_ENUM = names.PASCAL_SPACED_NO_ENUM

    @classmethod
    def set_entity_names_url_pascal(cls):
        # print(cls.ENTITY_ARG)
        nopath = cls.ENTITY_ARG.split("/")[-1]
        nopath_noext = nopath.split(".")[0]
        cls.set_entity_names_from_pascal(nopath_noext)  # assume PascalCase

    @classmethod
    def set_entity_names_path_snake(cls):
        nopath = cls.ENTITY_ARG.split("/")[-1]
        nopath_noext = nopath.split(".")[0]
        pascal = cls.pascal_from_snake(nopath_noext)  # assume snake_case
        cls.set_entity_names_from_pascal(pascal)

    @classmethod
    def hacky_get_ts_type_and_init_from_name(cls, name):
        if name.endswith("_enum"):
            return ("string", "''")
        if name.endswith("_id"):
            return ("number", -1)
        return ("string", "''")

    # common properties/util settings
    TAB04 = "    "
    TAB08 = "        "
    TAB12 = "            "
    TAB16 = "                "
    TABLES_SQL = {}
