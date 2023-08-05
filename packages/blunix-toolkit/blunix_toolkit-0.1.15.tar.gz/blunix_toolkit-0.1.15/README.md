# Blunix Toolkit

The Blunix Toolkit is a collection of Python glue-code that helps our
engineering team to uniformly collaborate on the development of the
already 100+ repositories we are maintaining inside our Github
organization.

The code is currently still undergoing rapid development and thus isn't
publicly distributed anywhere, yet. As of now, simply use the included
`Makefile` to install/uninstall the package. Make sure to create a
virtualenv before installing.

```bash
mkvirtualenv blunix-toolkit
setvirtualenvproject
make install    # or uninstall, respectively
```

When the configuration file is accessed for the very first time, the
toolkit will ask you a set of questions regarding your name, email,
Github account, as well as your local development workspace layout.

Your answers will be marshaled to `~/.config/blunix/blunix.yaml`. This
is your individual Blunix engineering configuration file. Have a look at
it with:

```bash
blunix-config-edit
```

Please note, that you will need to use an
[API access token](https://github.com/settings/tokens) as your
Github password if you have enabled 2FA.

The toolkit core consists of a set of Python packages and modules around above
stated configuration file, as well as executable entry-point scripts that
leverage this API. These scripts can be found in the `bin/` directory.

In addition to this "core", it is possible to extend the local $SHELL
with some very useful environment variables and shell functions.

```bash
# Generate the shell-code
blunix-config-bash

# or automatically source it like this
source <(blunix-config-bash)
```

Take a look at your new environment. You should see all sorts of `BLUNIX_*`
variables and more.

```bash
set | grep -i blunix
```

# Getting started

Once your configuration file has been created you can run a set of useful
Github API requests, such as:

```bash
# list all repositories
blunix-gh-repos

# list all role-* repositories
blunix-gh-roles

# list all playbook-* repositories
blunix-gh-playbooks
```

You can now combine these scripts with the above shell-magic:

```bash
# Clone all role-* repositories to your $BLUNIX_ROOT_DIR_ROLES directory while
# additionally creating a virtualenv for each repo and setting the project
# directory to the repositories workspace directory.
blunix-gh-roles | cut -d/ -f2 | blunixForEach 'cd "$BLUNIX_ROOT_DIR_ROLES"; blunixWorkon "$item"'

# Similar to the above, you can do the same with all Github playbook-* repositories.
blunix-gh-playbooks | cut -d/ -f2 | blunixForEach 'cd "$BLUNIX_ROOT_DIR_PLAYBOOKS"; blunixWorkon "$item"'
```
