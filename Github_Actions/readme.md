GitHub Actions setup is made of: event, workflow, job, step, and runner.

![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

## Example workflow:
```
name: pixelpost CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Say hello
        run: echo "hello from CI"
```

![alt text](image-3.png)

Install actionlint to verify linting errors:

actionlint --version || (cd /usr/local/bin && curl -fsSL https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash | bash)
```
mkdir -p /root/demo/.github/workflows
cat > /root/demo/.github/workflows/ci.yml <<'EOF'
name: demo CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Show message
        run: echo "CI is ready"
EOF
actionlint /root/demo/.github/workflows/ci.yml
```

![alt text](image-4.png)

![alt text](image-5.png)

![alt text](image-6.png)

![alt text](image-7.png)

```
name: CI for pixelpost
on: 
  push: 
    branches: [main]
  pull_request: 

jobs: 
  test: 
    runs-on: ubuntu-latest
    steps: 
      - name: run my choice
        run: echo "Hello"
```
* path filtering
```
name: pixel CI
on: 
  push:
    paths: 
      - 'docs/**'
jobs: 
  build-docs: 
    runs-on: ubuntu-latest 
    steps: 
      - name: any command
        run: echo "done"
```

* Cron schedule / workflow_dispatch
```
name: Nightly schedule
on: 
  schedule: 
    - cron: "0 2 * * *"
  workflow_dispatch: 
jobs: 
  full-tests: 
    runs-on: ubuntu-latest
    steps: 
      - name: run sanity
        run: "python main.py"
```
![alt text](image-8.png)

![alt text](image-9.png)

```
name: build something

on: push

jobs:
  job_1:
    runs-on: ubuntu-latest
    steps:
      - name: Print current date
        run: date
      - name: Print current working folder
        run: pwd
      - name: Print done message
        run: echo "Done"
```
![alt text](image-10.png)

```
name: multi-line
on: 
  push: 
jobs: 
  test: 
    runs-on: ubuntu-latest
    steps: 
      - name: Multi line
        run: |
          mkdir report
          date > report/report-generated-at.txt
          echo "Done"
      - name: list files
        shell: bash
        run: ls report
        working-directory: report
```

![alt text](image-11.png)

Actions can also live in the same repository through a local path, or come from a Docker image. Those forms use different uses: addresses; owner/repository@ref names a remote repository action.

The marketplace

Published actions are listed in the GitHub Marketplace at github.com/marketplace. There are actions for checking out code, setting up language toolchains, sending Slack messages, publishing releases, and much more. Before writing a long run script for a common task, it is normal to check whether a well maintained action already does it.

Anyone can publish an action, so the owner matters. Actions under the actions owner are maintained by GitHub and are the safe default for the basics.

In the next lesson: the one action almost every workflow starts with, and the reason it has to exist.

![alt text](image-12.png)

# Fix:
```
steps:
  - name: Get the code
    uses: actions/checkout@v4
  - name: Read the readme
    run: cat README.md
```

ex:
```
name: Checkout code
on: 
  push: 
jobs: 
  test: 
    runs-on: ubuntu-latest
    steps: 
      - name: checkout code
        uses: actions/checkout@v4
      - name: list files
        shell: bash
        run: ls
```
```
- name: Install Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
```

```
git config --global credential.helper store
login=$(curl -s -H "Authorization: token $(cat /root/.github/token)" \
  https://api.github.com/user | jq -r '.login // empty')
[ -n "$login" ] || { echo "No GitHub login - check /root/.github/token" >&2; exit 1; }
echo "https://${login}:$(cat /root/.github/token)@github.com" > /root/.git-credentials
chmod 600 /root/.git-credentials
```

![alt text](image-13.png)

![alt text](image-14.png)

![alt text](image-15.png)

![alt text](image-16.png)

![alt text](image-17.png)

![alt text](image-18.png)
![alt text](image-19.png)

# Composite action

![alt text](image-20.png)

![alt text](image-21.png)

That one difference decides everything else:

A composite action shares the job's runner, workspace, and environment. Files created by earlier steps are right there. A reusable workflow starts separate jobs with separate job workspaces. Do not rely on shared files, even if self-hosted jobs happen to use the same physical runner; pass data through defined inputs, outputs, artifacts, or secrets. Some caller context and the automatic GitHub token remain available by design.
A reusable workflow can contain several jobs, a matrix, and needs: chains. A composite action is only ever a flat list of steps.
A caller can pass declared secrets to a reusable workflow or use secrets: inherit where GitHub permits it. Environment secrets in the called job and the automatic GitHub token follow their own rules. A composite action has no secrets section - the calling workflow usually hands a needed secret in as an input or an environment variable.
A rule of thumb that holds up well: if the shared thing needs its own runner or several jobs, make it a reusable workflow. If it is a recipe of steps you want inside many jobs, make it a composite action. Teams commonly use both - a reusable workflow for the pipeline's shape, composite actions for the small recipes inside it.


```
tok=$(cat /root/.github/token)
login=$(curl -s -H "Authorization: token $tok" https://api.github.com/user | jq -r '.login // empty')
[ -n "$login" ] || { echo "No GitHub login - check /root/.github/token" >&2; exit 1; }
reg=$(curl -s -X POST -H "Authorization: token $tok" \
  "https://api.github.com/repos/$login/actions-deploy/actions/runners/registration-token" \
  | jq -r '.token // empty')
[ -n "$reg" ] || { echo "No registration token - does actions-deploy exist?" >&2; exit 1; }
cd /root/actions-runner
export RUNNER_ALLOW_RUNASROOT=1
./config.sh --unattended --replace \
  --url "https://github.com/$login/actions-deploy" \
  --token "$reg" --name "$(hostname)" --labels self-hosted --work _work \
  || { echo "config.sh did not register the runner" >&2; exit 1; }
# a re-run must be able to replace an earlier unit of the same name
systemctl stop escbash-gh-runner 2>/dev/null || true
systemctl reset-failed escbash-gh-runner 2>/dev/null || true
systemd-run --collect --unit=escbash-gh-runner \
  --setenv=RUNNER_ALLOW_RUNASROOT=1 \
  --working-directory=/root/actions-runner /root/actions-runner/run.sh
online=""
for i in $(seq 1 15); do
  if curl -sL -H "Authorization: token $tok" \
    "https://api.github.com/repos/$login/actions-deploy/actions/runners" \
    | jq -e --arg name "$(hostname)" \
      '[.runners[]? | select(.status == "online" and .name == $name)] | length > 0' \
      >/dev/null 2>&1; then
    online=yes; break
  fi
  sleep 2
done
[ -n "$online" ] || { echo "run.sh started but $(hostname) never reached status online" >&2; exit 1; }
echo "runner online"
```