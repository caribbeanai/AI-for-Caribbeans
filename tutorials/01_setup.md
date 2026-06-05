# Tutorial 1, Set up your environment

You need Python and a code editor. If you have neither, follow this.

## On macOS

1. Install Homebrew from brew.sh.
2. Run `brew install python git`.
3. Install VS Code from code.visualstudio.com.

## On Windows

1. Install Python from python.org. During install, tick "Add Python to PATH".
2. Install Git from git-scm.com.
3. Install VS Code.

## On Ubuntu or other Linux

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

## Clone this repo

```bash
git clone https://github.com/caribbeanai/ai-for-caribbeans.git
cd ai-for-caribbeans
```

## Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate     # macOS or Linux
# .venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Test it

```bash
python audiences/kids/kids_mango_sorter.py
```

If you see two predictions printed, your environment works.

## Optional: get an LLM API key

- Anthropic: sign up at anthropic.com, create a key, set it: `export ANTHROPIC_API_KEY=...`
- OpenAI: sign up at platform.openai.com, create a key, set it: `export OPENAI_API_KEY=...`

The repo's code reads these from the environment.
