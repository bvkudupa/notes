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