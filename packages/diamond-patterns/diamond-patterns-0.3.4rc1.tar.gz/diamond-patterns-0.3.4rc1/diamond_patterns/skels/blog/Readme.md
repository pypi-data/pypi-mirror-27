# website

Welcome to your blog.
This blog is based on Jekyll, the Ruby website generator.
The site generator works automatically with github pages.
Another mode of stand-alone operation is provided for any web/shell host via git hooks.

## Installation

This scaffold was originally built from http://github.com/iandennismiller/diamond-patterns.
In most situations, the `diamond` command line program would have been used:

    diamond --skel blog scaffold

To operate the Jekyll site generator on a remote web/shell provider, execute the following Makefile target in the local working copy of the project.

    make init

That Makefile target will use the scripts available in `_bin/` to create a git repository on a remote host, install git hooks, and start building the static site each time changes are pushed to the repository.
The effect is very similar to GitHub's implementation of their Jekyll-based site generator.

### Multiple git origin remotes

It is possible to have one git remote function as a site generator (e.g. a web/shell host) while having a second remote for project management (e.g. GitLab).
To have two git remotes, issue two `git remote set-url --add` commands:

    git remote -v
    git remote set-url --add --push origin ORIGINAL_URL
    git remote set-url --add --push origin SECOND_URL

## Usage

### Writing

Use the built-in template engine to create new posts:

    make new

### Publishing

Once the site is installed, deployment is as simple as pushing code to git.

    git add -A
    git commit -am "note about commit"
    git push

## Local development

To run the local server:

    make serve

The test website is available at [http://127.0.0.1:4000](http://127.0.0.1:4000).

### Regenerate javascript

A primitive form of JavaScript pre-processing is available through the use of Jekyll templates.
The files in `_js` can be rendered into a single file called `js/main.js` that is quicker to download.
The javascript pre-processor is invoked with:

    make js
