import os
import tempfile
import subprocess

def verbose(msg):
    if OPT_VERBOSE:
        print(f"[ {msg} ]")

def cleanup():
    if TMP_FILE and os.path.isfile(TMP_FILE):
        verbose("Clearing temp file")
        os.remove(TMP_FILE)

def die(msg):
    print(f"💀 {PROGNAME} !! {msg}")
    cleanup()
    exit(1)

def print_manual():
    print("""
Usage: $ PROGNAME command [-hv] [-l NUM]

Commands:

  new, add
          Opens up an empty buffer in your EDITOR.
          Then, provided it's not empty, PROGNAME will
          save the buffer in a shared record file.

  show, print, sh, pr
          Prints all saved notes in reverse
          chronological order to stdout.

  open, op
          Forwards the path to the record file
          as an argument to your EDITOR.

  delete, del
          PROGNAME will erase every saved note.

Options:

  -l NUM  Shows up to NUM entries (applicable only
          when printing to stdout).

  -h      Prints this help.

  -v      Shows verbose logs.

--
          PROGNAME uses XDG_DATA_HOME environment
          variable to determine the location of
          the record file.
""")

def read_record():
    with open(RECORD, "r") as file:
        records = file.read().split(TAG)
        records = [record.strip() for record in records if record.strip()]
        return records

def check_for_record():
    if not os.path.isfile(RECORD):
        die("No record exists")

def check_for_tty():
    if not os.isatty(0) or not os.isatty(1):
        die("stdin and stdout must both be ttys")

def get_word_count(filename):
    with open(filename, "r") as file:
        content = file.read()
        return len(content.split())

def print_record():
    records = read_record()
    if OPT_LIMIT > 0:
        verbose(f"Limit set to {OPT_LIMIT}")

        i = 0
        for record in records:
            i += 1
            if i > OPT_LIMIT:
                break
            print(f"{i:3}. {record}")
    else:
        for record in records:
            print(record)

def add_record():
    check_for_tty()
    TMP_FILE = tempfile.mktemp(suffix=".note.md")
    with open(TMP_FILE, "w") as file:
        subprocess.run([EDITOR, TMP_FILE])
    words = get_word_count(TMP_FILE)
    if words < 1:
        die("No words written, discarding note")
    verbose(f"Counted {words} words")
    os.makedirs(os.path.dirname(RECORD), exist_ok=True)
    with open(RECORD, "a") as record_file:
        record_file.write(f"{TAG} {TMP_FILE} {os.path.getctime(TMP_FILE)}\n")

# Implement other commands similarly

def main():
    if __name__ == "__main__":
        # Parse command-line arguments and set variables like NOTE_COMMAND, OPT_VERBOSE, OPT_LIMIT, etc.
        if NOTE_COMMAND in ["new", "add"]:
            add_record()
        elif NOTE_COMMAND in ["show", "print", "sh", "pr"]:
            check_for_record()
            print_record()
        elif NOTE_COMMAND in ["open", "op"]:
            check_for_record()
            check_for_tty()
            subprocess.run([EDITOR, RECORD])
        elif NOTE_COMMAND in ["delete", "del"]:
            if OPT_FORCE:
                if os.path.exists(RECORD):
                    os.remove(RECORD)
                    print("All saved notes have been deleted.")
                else:
                    print("No record exists.")
            else:
                die(f"Pass -f flag to delete {RECORD}")
        else:
            print_manual()
            die(f"Invalid command \"{NOTE_COMMAND}\"")

# Define the command-line arguments (example)
PROGNAME = "note_app.py"
TMP_FILE = None
NOTE_COMMAND = None
OPT_VERBOSE = False
OPT_LIMIT = 0
OPT_FORCE = False

# Get the value of EDITOR environment variable
EDITOR = os.environ.get("EDITOR")
if not EDITOR:
    die("EDITOR environment variable not defined.")

# Define the location of the record file
RECORD = os.path.join(os.path.expanduser("~/.local/share"), "note_record")
verbose(f"Record file at: {RECORD}")

TAG = "%=--=%"  # Separator used in records

if __name__ == "__main__":
    main()
