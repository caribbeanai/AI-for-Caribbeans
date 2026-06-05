"""
Sanity check the repo structure.

Author: Adrian Dunkley
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def count(glob):
    return len(list(ROOT.glob(glob)))


def main():
    print("AI for Caribbeans, repo health check")
    print(f"  Top level README:       {(ROOT / 'README.md').exists()}")
    print(f"  License:                {(ROOT / 'LICENSE').exists()}")
    print(f"  Authors:                {(ROOT / 'AUTHORS.md').exists()}")
    print(f"  Hero image:             {(ROOT / 'assets' / 'hero.svg').exists()}")
    print(f"  Country profiles:       {count('countries/*/README.md')}")
    print(f"  Course READMEs:         {count('courses/*/README.md')}")
    print(f"  Course lesson files:    {count('courses/*/lesson_*.md')}")
    print(f"  Application READMEs:    {count('applications/*/README.md')}")
    print(f"  Audience READMEs:       {count('audiences/*/README.md')}")
    print(f"  Prompt templates:       {count('prompt-templates/*.md')}")
    print(f"  Skills:                 {count('skills/*/SKILL.md')}")
    print(f"  Tutorials:              {count('tutorials/*.md')}")
    print(f"  Datasets:               {count('datasets/*.csv') + count('datasets/*.json')}")
    print(f"  Python files:           {count('**/*.py')}")


if __name__ == "__main__":
    main()
