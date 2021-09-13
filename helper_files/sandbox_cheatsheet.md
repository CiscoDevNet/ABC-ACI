# Guacamole tips
- Open the clipboard to paste from outside the sandbox:
> MAC: Ctrl+Command+Shift

> Windows: Ctrl+Alt+Shift

- Switch window short cut:
> Ubuntu: Super + tab

> MAC: Option + tab

- Application not opening? Kill it and try again.
> killall -9 <appname>

```bash
(py3venv) [developer@devbox ~]$ killall -9 code
(py3venv) [developer@devbox ~]$ killall -9 postman
```

# Linux commands cheatsheet (in the context of the training)

Change directory with cd.
By defining .., you get to the parent directory.
```bash
cd <path_to_your_directory>
cd .. #change to parent directory
```

List files in your directory. If you want to see hidden files, include option -a
```bash
ls
ls -a
```

Copy something from somewhere.
```bash
cp <source> <destination>
```

Create a directory
```bash
mkdir <directoryname>
```

Open a file in VS code (created if not exist)
```bash
code <my_file_name>
```