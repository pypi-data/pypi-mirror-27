# 3Blades Command Line Tools (CLI)


## Setup
Currently you need to use python 3.6. At some point I'll make it 2.7 and 3.4+ compatible.

- `pip3.6 install tbs-cli`

If you would like to use the CLI tools with our dev environment (or any other env for that matter):
`export TBS_API_URL="https://dev-api.3blades.ai"` or the appropriate URL. If you do not set this env var, production will be used.

## Usage

### Login
`tbs-cli login` -> You will be prompted for your username and password. This will create a `threeblades.token` file in your `$HOME` directory that will be used for subsequent logins. Delete this file if you would like to login as a different user, or to a different environment.

### Projects
`tbs-cli projects <sub command>`
Currently implemented sub-commands are: `list`, `create`, `detail`, and `delete`. You will be prompted for any required arguments. Flags (`--name`, etc.) will come at a later date.

### Deployments
`tbs-cli deployments <sub command>`
Currently accepted sub commands are: `create`.

Currently available runtimes:
- `python2.7`

Currently available frameworks:
- `tensorflow`

In order to deploy the model you've created at the command line, just send a `POST` request to `https://dev-api.3blades.ai/v1/<namespace>/projects/<project>/deployments/<deployment>/`. The ability to do this from the command line will be added very soon (in the next day or so).


**Note:** This document is very much a work in progress, and it will be updated rapidly for the forseeable future.
