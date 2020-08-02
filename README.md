# inkscape ExtensionDevTools

A short script developed for the development of Inkscape Extensions.

Usage:

Inside of your exensions folder:

    git clone https://github.com/dapperfu/inkscape_ExtensionDevTools.git

Add the following before your <etxension>.run():

```
if __name__ == "__main__":
    import inkscape_ExtensionDevTools

    inkscape_ExtensionDevTools.inkscape_run_debug()
```

Workflow:

1. Call Inkscape Extension from Inkscape.
2. Open extension folder in IDE (VSCode/Spyder/etc)
3. Open extension in IDE & add debug points.
3. Run ```<extension>_run.py``` in the debug folder.
4. Debug.
