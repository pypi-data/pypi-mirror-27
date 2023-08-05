## pubpub

A package to turn Jupyter ipynb files into pdf files

```bash
pubpub --help
```

```bash
pubpub run \
      -f "./book_drafts/Chapter 1.ipynb" \
      -f "./book_drafts/Chapter 2.ipynb" \
      -f "./book_drafts/Chapter 3.ipynb" \
      -f "./book_drafts/Chapter 4.ipynb" \
      -o ./print.pdf \
      -v udeeply \
      --template ./fullstack.tplx
```

Alternatively, all these options can be specified in a `book.md` file:

For instance:

```markdown
---
title: Zero to Deep Learning
template: gen_template.tplx
virtualenv: ztdlbook
asset_files:
  - ./assets:../assets
authors:
  - Francesco Mosconi
  - Ari Lerner
---

./course/1_Getting_Started.ipynb
./course/2_Data_Manipulation.ipynb
```

We can then run this with the following command:

```bash
pubpub latex -f ./test/book.md -o /tmp/complete.pdf
```

## How to run

Install the required dependencies:

```bash
# ubuntu
sudo apt-get update -yq && sudo apt-get install -yq texlive-latex-extra texlive-latex-base
```

## Install pubpub

```bash
pip install --upgrade pubpub
```



