from PyInstaller import __version__
from PyInstaller import log as logging
from PyInstaller import compat
from PyInstaller.__main__ import generate_parser, run_makespec, run_build

import os
import platform
import re
from pathlib import Path

logger = logging.getLogger(__name__)

def make_all_spec_file(spec_files: list, all_spec_name: str = 'all', all_spec_path: str = '') -> str:
    s_all = ""
    coll_all = []
    j0 = None
    for i, spec_file_path in enumerate(spec_files):
        specFile = Path(spec_file_path)
        s = specFile.read_text()
        for v in ["a", "pyz", "exe", "coll"]:
            vi = "{}{}".format(v, i+1)
            s = re.sub("\\b{}\\s*=".format(v), "{} =".format(vi), s)
            s = re.sub("([(,]|\\s){}([),.])".format(v), "\\1{}\\2".format(vi), s)
        p = "\\bcoll{}\\s*=\\s*COLLECT\\(".format(i+1)
        m = re.search(p, s)
        if m:
            coll_start = m.start()
            coll_content = m.end()
            coll_end = s.find(")\n", coll_content)
            if coll_end:
                coll_s = s[coll_content:coll_end]
                s = s[:coll_start] + s[coll_end+2:]
                coll = list(l.strip()+"," for l in coll_s.split(',') if len(l.strip()) > 0)
                if i == 0:
                    coll_all = coll
                for j, l in enumerate(coll):
                    if re.search("\\b(exe|a){}([,.])".format(i+1), l):
                        if i > 0:
                            if j0 is None:
                                coll_all.append(l)
                            else:
                                coll_all.insert(j0, l)
                                j0 += 1
                    else:
                        if i == 0:
                            if j0 is None:
                                j0 = j
        if i > 0:
            s1 = ""
            for v in ["a", "pyz", "exe"]:
                p = "\\b{}{}\\s*=".format(v, i+1)
                m = re.search(p, s)
                if m:
                    v_start = m.start()
                    v_end = s.find(")\n", v_start)
                    if v_end:
                        s1 += "\n" + s[v_start:v_end+2]
            s = s1
        s_all += s + "\n"
    if len(coll_all) > 0:
        s_all += "\ncoll = COLLECT(\n    " + "\n    ".join(coll_all) + "\n)\n"

    all_spec_file = os.path.join(all_spec_path, all_spec_name + '.spec')
    with open(all_spec_file, 'w', encoding='utf-8') as specfile:
        specfile.write(s_all)
    return all_spec_file

def make_all_installer(pyi_args_list: list, all_spec_name: str = 'all', all_spec_path: str = None, pyi_config: dict = None) -> str:
    compat.check_requirements()

    import PyInstaller.log

    spec_files = []

    try:
        args0 = None

        for pyi_args in pyi_args_list:
            parser = generate_parser()
            args = parser.parse_args(pyi_args)

            if args0 is None:
                PyInstaller.log.__process_options(parser, args)

                # Print PyInstaller version, Python version, and platform as the first line to stdout. This helps us identify
                # PyInstaller, Python, and platform version when users report issues.
                logger.info('PyInstaller: %s' % __version__)
                logger.info('Python: %s%s', platform.python_version(), " (conda)" if compat.is_conda else "")
                logger.info('Platform: %s' % platform.platform())

            # Skip creating .spec when .spec file is supplied.
            if args.filenames[0].endswith('.spec'):
                parser._forbid_options(
                    args, group="makespec", errmsg="makespec options not valid when a .spec file is given"
                )
                spec_file = args.filenames[0]
            else:
                spec_file = run_makespec(**vars(args))

            spec_files.append(spec_file)

            if args0 is None:
                args0 = args

                if all_spec_path is None:
                    all_spec_path = str(Path(spec_file).parent)

        if args0 is None:
            return None

        all_spec_file = make_all_spec_file(spec_files, all_spec_name, all_spec_path)

        run_build(pyi_config, all_spec_file, **vars(args0))
        return all_spec_file

    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")
    except RecursionError:
        from PyInstaller import _recursion_too_deep_message
        _recursion_too_deep_message.raise_with_msg()
