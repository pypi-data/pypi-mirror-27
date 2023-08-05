* Version 0.2.2 (2017-11-25)

    * Plugins
        * Actions
            * command: Add an `strace` option, to enable/disable strace
              profiling (to automatically set file dependencies). This can
              be enabled/disabled separately for each file.
        * Renderers
            * html and htmlplus: Add current date to the generated html
              code.

    -- Louis Paternault <spalax+python@gresille.org>

* Version 0.2.1 (2017-08-25)

    * Core
        * `.evsignore` files now accepts comments (starting with #) and
          blank lines.
        * Syntax errors in `.evsignore` files are now nicely catched.
    * Plugins
        * Renderer
            * htmlplus: Add option `display_log` (decide wether logs are
              displayed always, never, only when compilation fails).

    -- Louis Paternault <spalax+python@gresille.org>

* Version 0.2.0 (2017-07-27)

    * Installation
        * Various setup improvements.
    * Core
        * Add python3.6 support.
        * Change python library used to interact with git repository (was
          pygit2; is now gitpython).
        * Configuration files are now read in unicode; files are now
          written in unicode.
        * Deleting an empty cache is allowed.
        * Improve changelog formatting
        * hooks: Refactor context managers (closes #64)
    * Command line
        * Binaries are written in `__main__.py` modules, and can be called
          using `python -m evariste.MY.MODULE`.
        * The `evariste` binary is now an alias for `evs compile` (closes
          #63).
        * Catch errors in CLI arguments (closes #65).
        * Raise a nice error when no subcommand is provided (closes #56).
    * Plugins
        * Improve plugin API (closes #55).
        * Actions
            * autocmd: New plugin (closes #23).
            * command: Internal simplification and improvements.
            * make: New plugin (closes #33).
        * VCS
            * Only one VCS plugin can be enabled at a time (closes #61).
            * fs: New plugin (closes #41).
            * git: Speed file analysis.
        * Renderers
            * text:
                * Add option `reverse` (closes #66).
                * Add option `display` (closes #62).
            * htmlbox:
                * Renamed to `htmlplus`, with better CSS and javascript.
                * Set `page.tmpl` as the default template (closes #67).
                * Add an easy way to customize templates (closes #68).
                * Compilation log is now displayed (closes #18).
            * html.readme.mdwn: New plugin (closes #74).
    * Tests
        * More tests.
        * Use continuous integration (gitlab-CI).

    -- Louis Paternault <spalax+python@gresille.org>

* Version 0.1.0 (2015-08-17)

    * Licence: Switched from GPL to AGPL.
    * Various setup.py improvements
    * Core
        * Python 3.5 support
        * Implemented multiprocessing
        * Sanitize the way path are handled
        * Many many internal fixes and improvements.
        * Now uses pygit2 version 0.22
    * Plugins
        * Improved management and loading
        * Added hooks
        * Improved selection (enable/disable setup options, default and
          required plugins, dependencies).
        * Renderers
            * htmllog: Removed draft. Will be addded later.
            * htmlplus: New html renderer, with CSS.
            * html: Various improvements.
            * text: New simple text renderer.
        * VCS
            * Git: Improved support (submodules, files added but not
              committed, code speed, etc.)
        * Actions
            * LaTeX: Various improvements.
            * Raw: Changed default behavior. By default, everything is
              rendered.
            * Command
                * Fixed bugs with shell commands (quotes and ampersands
                  are now supported)
                * Merged command and multicommand actions into command
    * Command line
        * Compilation is independent from current working directory
        * Added -j and -B options
        * Default value for arguments can be set in setup file
    * Tests
        * Wrote tests. Will be completed in next version.
    * Documentation
        * Wrote draft
    * evs tools
        * New evs tool
        * New evs-cache tool

    -- Louis Paternault <spalax+python@gresille.org>

* Version 0.0.0 (2015-03-20)

    * First published version. Works, but with few options, and no
      documentation.

    -- Louis Paternault <spalax+python@gresille.org>
