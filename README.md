# Tachi

**Tachi** is a simple Command-Line Interface (CLI) tool for managing projects.  
It allows you to add projects, list them, and manage configuration settings.  
The project is designed in a modular way for easy maintenance and scalability.

## Installation

1. Clone the repository:

```bash
git clone git@github.com:amirabroun/tachi.git
```

```bash
cd tachi
```

2. Run the installer script:

```bash
./install.sh
```

This script will:

- Find the `__main__.py` file
- Add a `tachi` alias to your shell (`bash` or `zsh`)
- Load the shell configuration so you can use `tachi` immediately

## Usage

After installation, you can run Tachi from anywhere using:

```bash
tachi
```

Some example commands:

```bash
tachi add-project
tachi list-projects
tachi config
```

## Requirements

- Python 3.x
- Bash or Zsh shell