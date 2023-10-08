Pre-requisites [ One-time step ]
---------------

#### 1. git setup section for windows with powershell.

This is one time setup that is needed to get the ssh private/public keys.
Install git for windows, then run the below in powershell.

```
ssh-keygen -t rsa -b 4096 -C "<username>@domainname.com"
sc.exe create sshd binPath=C:\Windows\System32\OpenSSH\ssh.exe
ssh-add ${HOME}\.ssh\id_rsa
```

Force git to checkout as-is and commit in linux LF.
```
git config --global core.autocrlf input
```

Goto - https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/#SetupanSSHkey-ssh1

Follow steps to add ssh public key into bitbucket.

#### 2. Install Docker for windows

https://hub.docker.com/editions/community/docker-ce-desktop-windows/

#### 3. Install VSCode

https://code.visualstudio.com/

Type
```
Ctrl+Shift+p -> Type in "Extensions: Install Extensions"
```

Then install following extensions in vscode.

- Docker
- Python
- Pylynce
- WSL
- WSL Distro
- Remote - Containers
- Dev Container
- YAML
