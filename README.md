# avo-plugin-demo
Information about and examples of (Python) plugins for Avogadro 2 to demonstrate the revamped plugin API in v2.0 onwards

## A brief outline of Avogadro's plugin API

### Basic requirements

- For now, plugins for Avogadro must be written in Python
    - Support for other languages may come at a later date; in particular, binary plugins would be of interest (though these would not be distributed via Avogadro's infrastructure due to security concerns)
- The installed form of a plugin used by Avogadro consists of a single directory bearing the plugin's name and containing a metadata file (see below) as well as all the plugin's source code in one of the three forms described below
- Plugins may only have `A-Z, a-z, 0-9, -` i.e. ASCII letters, numbers, and the hyphen minus, in their names (no Unicode, no underscores, no other punctuation or whitespace)
    - Underscores are substituted for hyphens in any situations where it is necessary, but the canonical name uses hyphens only
- All plugin files, and communication over the Avogadro-plugin interface, must be exclusively in UTF-8

### Plugin types

- There are **three sub-types** of Python plugin:
    1. Script(s)
    2. Python package
    3. Pixi project
- Note: unlike Avogadro 1.102 and earlier, single-file scripts with no metadata are no longer allowed – all scripts must be within their own folder with a metadata file, making them a proper plugin (even if the folder only contains a single script)

#### Script plugins (`pyscript`)

- A script plugin consists of one or more Python scripts collected into a single bundle in a folder, allowing for easy installation, deinstallation, management, and distribution
- Regardless of the number of scripts, a *single* metadata file (see below) is required for the plugin as a whole and must be located in the folder next to the scripts
- The plugin is not allowed to have any dependencies
- Script plugins are invoked by Avogadro by each script being run individually via the **script API**

#### Package plugins (`pypkg`)

- A package plugin for Avogadro is essentially a standard Python package as found in the wider ecosystem -- specifically, it consists of a directory that contains the source code for a Python *distribution* package, that can be built and installed by `pip`, `poetry`, `uv` etc.
- Metadata for Avogadro is generally contained in the package's `pyproject.toml`
- The plugin may use dependencies from the PyPI repository
- The plugin may use any structure for its source code that works for a Python package – the two most common structures are the so-called "flat" and "src" layouts
- Avogadro will install the plugin as a Python package to a Python virtual environment in one of two places (to be decided):
    1. The main Avogadro environment
        - Allows shared dependencies
        - Means code has to be written to account for the possibility that installation fails due to dependency conflicts
    2. A plugin-specific environment contained within the plugin's own folder
- Package plugins are invoked by Avogadro using the **package API**

#### Pixi project (`pypixi`)

- Pixi project plugins consist of a single directory containing a Pixi project, with a `pyproject.toml` file used as the Pixi environment manifest
- Metadata for Avogadro is generally contained in the project's `pyproject.toml`
- The plugin may use dependencies from the Conda ecosystem, as well as from the usual PyPI repository
- A plugin-specific Pixi environment is initialized for the plugin in its own directory, and all its dependencies are installed using Pixi
- Pixi plugins are also invoked by Avogadro using the **package API**

### Metadata and configuration

- Metadata that Avogadro needs to know in order to properly run a plugin was until now obtained dynamically by running the plugin
- Instead, metadata is now extracted from static TOML files
    - `plugin.json` is deprecated
- The static metadata for a plugin contains the following information:
    - The type of plugin
    - The features provided by the plugin, the types of each plugin feature (`file-formats`, `menu-commands` etc.), and various information about each feature e.g. what the display names and/or menu paths for each of those items should be
    - Info about the plugin's provenance that was previously in `plugin.json` e.g. author, version number
    - Whether or not the plugin wants a configuration to be recorded for it in the main Avogadro configuration file, and if so, what entries the config should have for the plugin
- The metadata file may be in the form of:
    - `pyproject.toml` – the normal project metadata file in use in the modern Python ecosystem
        - plugin metadata for consumption by Avogadro is listed in the `[tool.avogadro]` table
        - some information is read from the normal `[package]` table e.g. the author information
    - `avogadro.toml` – an Avogadro-specific metadata file
        - metadata is all stored at the top level of the file (see the examples in this repository)
- For Python plugins, it is recommended to use `pyproject.toml` as the metadata file.
    - If preferable, Python plugins may also use `avogadro.toml`. If both `avogadro.toml` and `pyproject.toml` are found in the plugin's directory, `avogadro.toml` will take precedence and `pyproject.toml` will be ignored.
- For non-Python plugins, `avogadro.toml` must be used.

### Feature types

- Plugins can provide any number of the following features:

| Feature type         | TOML key               | Purpose                       |
| -------------------- | ---------------------- | --------------------------------- |
| Electrostatic Models | `electrostatic-models` | Provide models for Avogadro to use in the calculation of partial charges and/or electrostatic potentials |
| Energy Models        | `energy-models`        | Provide models for Avogadro to use in the calculation of energies and gradients |
| File Formats         | `file-formats`         | Parse chemical file formats that Avogadro doesn't know |
| Input Generators     | `input-generators`     | Prepare input files for computational chemistry programs |
| Menu Commands        | `menu-commands`        | Add additional items for the menus that carry out various tasks |

### The online plugin repository/index

- The Avogadro team continues to provide a central index of plugins, that can then be browsed and installed from within the plugin manager in the Avogadro UI
- The index has until now been hosted at https://avogadro.cc/plugins.json; the future location has yet to be decided
- The index is in future to be regularly updated in an automated fashion from the `repositories.toml` file in the GitHub repository at https://github.com/Avogadro/plugins
- Contributions of open-source plugins to the index is most welcome, and are made by opening a pull request that adds information on the plugin to the `repositories.toml` file in the `Avogadro/plugins` repo
- Each plugin listed on the index has its own table within `repositories.toml`. Each plugin has to specify (at minimum, suggestions welcome):
    - The git repository
    - The specific commit
    - Possibly a SHA256 hash that Avogadro can use to check the plugin files after download
    - The type of plugin, one of:
        - `py-scripts`
        - `py-pkg`
        - `py-pixi`
- Updates to plugins are likewise submitted to the index by submitting a PR to update the commit listed in `repositories.toml`
    - This improves security in comparison to the old index as the code for the plugin can't just be changed and delivered to all future plugin users without approval from the Avogadro team
- The new API thus uses a new file to hold information on the plugin repositories; this means we can keep the old one for a little while if we like, to avoid breaking plugins for older versions just yet

### The layout of Avogadro's local plugin directory

- Avogadro's data is stored under `<USERDATA>/OpenChemistry/Avogadro/`, where `<USERDATA>` is platform-specific. This location will be referred to as `.` throughout the rest of the document.
- Installed plugins are stored in subfolders under `./plugins/`:
    - `plugins/python/` for plugins written in Python

### How plugins are run

- Plugin functionality is invoked by Avogadro via two different APIs:
    1. Script API
    2. Package API
- Each feature that a plugin offers has an `identifier` as listed in the plugin's metadata file
- Features of a script plugin are invoked by Avogadro using `pixi run python plugins/python/<plugin>/<identifier>.py [OPTIONS]`
- Features of packages (including Pixi projects) are invoked using `pixi run avogadro-<plugin> <identifier> [OPTIONS]`
    - e.g. for the `mass` feature of a plugin called `demo` the full command would be `pixi run avogadro-demo mass`
    - The plugin defines an entry point in their `pyproject.toml` for the plugin's name prefixed with `avogadro-` e.g. for a `demo` plugin:
```toml
[project.scripts]
avogadro-demo = "demo:main"
```
- A plugin is required to correctly process certain option flags (by which it is meant that the plugin should not crash or error):
    - `--lang` – though actually changing behaviour based on the accompanying localization string is not obligatory
    - `--debug` – again, a change in behaviour is not obligatory, though plugins are encouraged to provide more detailed logs and error messages if this flag is passed
    - `--print-options` – *only* if the plugin indicates that the interface of a feature's dialog is to be specified *dynamically* using `user-options = "dynamic"`, it must respond appropriately to the flag, otherwise it does not need to as it will never be passed
    - `electrostatic-models` features must respond appropriately (according to what they support) to:
        - `--charges`
        - `--potential`
    - `file-formats` features must respond appropriately (according to what they support) to:
        - `--read`
        - `--write`
- All other option flags used in the plugin API until now are deprecated
    - `--run-command` and similar are no longer used; if a feature type only ever responds to one kind of request, no flag is needed, it is assumed to be the desired request
    - The information provided by things like `--display-name` and `--menu-path`, is now contained in the static metadata
- Avogadro will now *always* pass a JSON object as the main argument (following the feature identifier) to all feature types – for details of the contents, see below
    - This is no longer passed on `stdin`; streams of subsequent data are, however, if relevant for the plugin type
- Avogadro will now *always* accept an JSON object as the output of the plugin to `stdout` – for details of the contents, see below
    - If Avogadro expects a stream of output on `stdout`, it will first expect a JSON object as the initial output before the stream, and will handle any subsequent JSON object on `stdout` as an indication that the plugin process should be stopped

#### The input JSON

| Key                               | JSON data type        | Value                                                     | Feature types                         | Applicable    |
| ---                               | ---                   | ---                                                       | ---                                   | ---           |
| `config`                          | `object`              | The user's stored configuration of the plugin             | All                                   | `user-config` is specified |
| `cjson`                           | `object`              | The current CJSON file in full                            | All except `file-formats`             | `input-cjson = true` or `input-format = "cjson"` |
| `xyz`, `cml`, `pdb`, `cif`, `sdf`, `mdl`, `mol`, etc. | `string` | The contents of a file in the respective format    | All except `file-formats`             | `input-format = <fmt>` |
| `file`                            | `string`              | A path to a file in the filesystem                        | `file-formats`                        | Always        |
| `options`                         | `object`              | Key/value pairs for each option requested in `user-options` | `menu-commands`, `input-generators` | Always        |
| `points`                          | `array` of `number`   | The coordinates of the requested points                   | `electrostatic-models`                | Called with `--potentials` |
| `selectedAtoms`                   | `array` of `number`   | The indices of the atoms that are currently selected      | `menu-commands`                       | Always        |

#### The output JSON

| Key                               | JSON data type        | Value                                                     | Feature types             | Applicable    |
| ---                               | ---                   | ---                                                       | ---                       | ---           |
| `message`                         | `string`              | A message to display to the user in a pop-up dialog       | All                       | Always        |
| `error`                           | `string`              | Similar, but displays an error, and the plugin is stopped | All                       | Always        |
| `config`                          | `object`              | The user's configuration of the plugin as it should be saved | All                    | `user-config` is specified |
| `cjson`                           | `object`              | A CJSON file to be loaded                                 | All?                      | `output-format = "cjson"` |
| `xyz`, `cml`, `pdb`, `cif`, `sdf`, `mdl`, `mol`, etc. | `string` | The contents of a file in the respective format    | All?                      | `output-format = <fmt>` |
| `charges`                         | `array` of `number`   | The partial charges on each atom                          | `electrostatic-models`    | Called with `--charges` |
| `potentials`                      | `array` of `number`   | The electrostatic potential at each requested point       | `electrostatic-models`    | Called with `--potentials` |
| `bond`                            | `bool`                | Whether Avogadro should run automatic bond perception     | `menu-commands`           | Always        |
| `selectedAtoms`                   | `array` of `number`   | The indices of the atoms that Avogadro should select      | `menu-commands`           | Always        |
| `warnings`                        | `array` of `string`   | Non-fatal warnings to be shown in the generator's dialog  | `input-generators`        | Always        |
| `generatedFiles`                  | `object`              | Details of several files                                  | `input-generators`        | Always        |
| `mainFile`                        | `string`              | The primary input file for a calculation                  | `input-generators`        | Always        |

### Runtime plugin loading

- The process of loading, running, and installing plugins in Avogadro is streamlined significantly:
    - At launch:
        - No plugin is run
        - No Python interpreter is used
        - The plugin directories are scanned for plugins, and each TOML file found is parsed appropriately to get the metadata of each
            - (Hopefully) much faster than spinning up several Python processes for each plugin in turn just to request information like the display name
    - When a plugin needs to be run (because it's the selected force field, or because its menu option was selected), Avogadro just runs it according to the provided metadata
    - When downloading a plugin, Avogadro already knows the appropriate place to put it from the information in the plugin index on https://avogadro.cc
- The metadata will likely be cached in an index
    - That way, the scanning step on launch is skipped altogether
    - It's impossible to have a situation where a Python plugin is present but not installed
    - To cache the metadata:
        - A local plugin index in the form of a `plugins.toml` file would probably be maintained in the `plugins/` folder i.e. at `OpenChemistry/Avogadro/plugins/plugins.toml`
        - The local index would collate all the metadata from all the installed plugins
        - Note this requires a TOML writing library! It could also just be stored as JSON, but it seems a bit silly not to keep it consistent with the plugin metadata format
    - At launch, Avogadro would then just read the local cached index and does no scanning of the directory tree – the index has everything Avogadro needs to know
    - Plugin discovery/index generation/Python package installation is then only carried out at launch if there is no index found
    - Downloading a plugin using the built-in downloader causes the plugin to be installed (if it's a Python plugin) as well as appending the metadata to the index
    - Plugin discovery/index regeneration/reinstallation of all Python plugin packages ought to be manually triggerable via a menu option in the Avogadro interface

### Some Pixi usage notes

- Errors occurred when using Pixi's default build system (`hatchling`), works fine after switching to `uv_build`
    - However, at a later date it worked fine with `hatchling`
- Most reliable way to specify manifest path is with `pixi <command> --manifest-path <manifest> [ARGUMENTS]`
    - Specifying `--manifest-path` before the command doesn't work, not a global option for `pixi`, but is a global option for most of the pixi commands
    - Specifying `--manifest-path` after everything else works with `pixi add` but not with `pixi run`
- Have one Avogadro manifest in the plugins directory with an associated environment, plus one for each package and pixi plugin (or just each pixi plugin?)
- Script plugins:
    - Not installed/added to anything, run in the main Avogadro environment
    - Run using `pixi run --manifest-path <avo-manifest> python <plugin-dir>/<identifier>.py`?
- Python plugins:
    - Installed to ("added" to, in pixi terms) and run in the main Avogadro environment? Or should each plugin have its own virtual environment as standard practice?
    - Initialization of Avogadro environment done once, not for each plugin, pixi then keeps it up-to-date every time something is added, run etc.
    - Add to env using `pixi add --manifest-path <avo-manifest> --pypi "<plugin-name> @ file:///home/absolute/path/to/dir/of/plugin-name"`
    - Run using `pixi run --manifest-path <avo-manifest> plugin-name <identifier>`
- Pixi plugins:
    - Installed to and run in their own environment
    - Initialize environment using `pixi install --manifest-path <plugin-dir>/pyproject.toml`
    - Run in own env so no need to "add" to anything
    - Run using `pixi run --manifest-path <plugin-dir>/pyproject.toml plugin-name <identifier>`
