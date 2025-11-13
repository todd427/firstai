# Foundation F1 — Linux & Bash Basics
*30–60 minutes | Beginner-friendly | Works in WSL or Ubuntu*

## Objectives
- Navigate files and folders with confidence
- Edit files from the terminal
- Manage processes and permissions
- Understand paths, environment variables, and the shell profile

## Prerequisites
Module 2 (WSL/Ubuntu installed). Open a terminal.

## 1) The Five Moves
```bash
pwd          # where am I?
ls -la       # list files (long, all)
cd ~         # go home (tilde is your home)
cd /tmp      # absolute path
cd ..        # up one directory
```

## 2) Files & Folders
```bash
mkdir -p projects/your-first-ai
touch notes.txt
echo "hello" >> notes.txt
cat notes.txt
cp notes.txt notes.bak
mv notes.bak archive.txt
rm archive.txt              # beware: no trashcan
rm -r old_folder            # recursive delete
```

**Globs:** `*.py`, `data/*.json`  
**Hidden files:** start with `.` (e.g., `.env`, `.gitignore`).

## 3) Paths & Environment
```bash
echo $HOME
echo $PATH | tr ':' '\n' | nl
export EDITOR=nano
echo 'export EDITOR=nano' >> ~/.bashrc   # persist setting
source ~/.bashrc
```

## 4) Permissions & Ownership (crash course)
```bash
ls -l script.sh       # -rwxr-xr-- (u/g/o)
chmod +x script.sh    # add execute for user
chmod 644 file.txt    # rw-r--r-- (common for text files)
sudo chown $USER:$USER file.txt
```

## 5) Processes & Ports
```bash
ps aux | head
top                     # press q to quit
kill -9 <PID>           # force kill (last resort)
ss -ltnp | head         # show listening TCP ports
```

## 6) Editors: nano & vim
```bash
nano file.txt           # Ctrl+O save, Ctrl+X exit
vim file.txt            # i insert, Esc, :w write, :q quit
```

## 7) Search like a pro
```bash
grep -R "uvicorn" .
grep -Rni "TODO" .      # n=number, i=ignore case
find . -name "*.py" -maxdepth 2
```

## 8) Archives
```bash
tar -czf site.tgz static/     # create
tar -xzf site.tgz             # extract
unzip file.zip                # unzip zip files
```

## 9) Networking quickies
```bash
curl -I http://localhost:8000/health
ping -c 3 example.com
```

## 10) Checkpoint
- You can create `~/projects/f1demo`, add `hello.txt`, and list it with `ls -la`.
- `EDITOR` persists after opening a new terminal.
- You can kill a stuck process and confirm the port is free.

## Exercises
1. Make `~/sandbox/f1`, create three files, and move them into a `data` subfolder.
2. Write a two‑line shell script `sayhi.sh` that prints your name; make it executable and run it.
3. Use `grep -Rni` to find the word “generate” in your project.

## Troubleshooting
- **Permission denied** — try `chmod +x` for scripts, avoid `sudo` unless necessary.
- **Command not found** — run `sudo apt update && sudo apt -y install <tool>`.
- **PATH confusion** — echo `$PATH`, then add a folder using `export PATH="$HOME/bin:$PATH"` in `~/.bashrc`.
