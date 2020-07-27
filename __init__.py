def inkscape_run_debug():
    import sys
    import os
    import datetime
    import shutil

    # If we aren't calling this from our own script.
    if os.environ.get("DEBUG_RECURSION", "0") == "1":
        return
    script_path = os.path.abspath(sys.argv[0])
    debug_dir = os.path.join(os.path.dirname(script_path), "debug")
    os.makedirs(debug_dir, exist_ok=True)
    base_name, _ = os.path.splitext(os.path.basename(script_path))

    # Debug Information.
    with open(os.path.join(debug_dir, f"{base_name}.debug"), "w") as fid:
        fid.write("#" * 20)
        fid.write("\n# ")
        fid.write(str(datetime.datetime.now()))
        fid.write("\n")
        fid.write("#" * 20)

        fid.write("\nExecutable: \n\t")
        fid.write(sys.executable)

        fid.write("\nCurrentDirectory: \n\t")
        fid.write(os.path.abspath(os.path.curdir))

        fid.write("\nPaths:\n")
        for path in sys.path:
            fid.write("\t")
            fid.write(path)
            fid.write("\n")

        fid.write("\nArgs:\n")
        for arg in sys.argv:
            fid.write("\t")
            fid.write(arg)
            fid.write("\n")

    # Copy the temporary file to a permanent location for debugging.
    in_file = sys.argv[-1]
    if not in_file.endswith(".svg"):
        out_file = os.path.join(debug_dir, "input_file.svg")
        shutil.copy2(sys.argv[-1], out_file)
    else:
        out_file = in_file

    # Script to run Inkscape Extension as a Python script.
    with open(os.path.join(debug_dir, f"{base_name}.sh"), "w") as fid:
        fid.write("#!/usr/bin/env bash")
        fid.write("\n# ")
        fid.write(str(datetime.datetime.now()))
        fid.write("\n" * 2)
        fid.write("export DEBUG_RECURSION=1\n")
        fid.write("export PYTHONPATH=")
        fid.write(os.pathsep.join(sys.path))
        fid.write("\n")
        fid.write(sys.executable)
        fid.write(" ")
        fid.write(os.path.abspath(sys.argv[0]))

    # Python program to programmatically call the Inkscape Extension (with the same settings)
    # Useful for debugging an extension with VSCode or other debugger.
    with open(os.path.join(debug_dir, f"{base_name}_run.py"), "w") as fid:
        fid.write("#!" + sys.executable)
        fid.write(f"\n# {datetime.datetime.now()}\n")
        for module in ["sys", "os"]:
            fid.write(f"import {module}\n")
        for sys_path in list(sys.path):
            if len(sys_path) == 0:
                continue
            fid.write(f"sys.path.append('{sys_path}')\n")

        fid.write("args = [\n")
        for arg in sys.argv[1:-1]:
            fid.write(f'    "{arg}",\n')
        fid.write(f'    "{out_file}"\n')
        fid.write("]\n")

        fid.write(
            f"""
# Run the extension.
import {base_name} as extension
# Find the inkex.Effect class
for item in dir(extension):
    # Brute force looking for 'run' attribute.
    if hasattr(getattr(extension, item), "run"):
        # Create an instance of the extension.
        extension_instance = getattr(extension, item)()
        # Run the extension with the given arguments.
        output = os.path.join("{debug_dir}", "output_file.svg")
        extension_instance.run(
            args = args,
            output = output)
        break
"""
        )
