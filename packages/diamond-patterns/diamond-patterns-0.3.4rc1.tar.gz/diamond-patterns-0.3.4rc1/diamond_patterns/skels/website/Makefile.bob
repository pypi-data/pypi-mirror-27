# {{{ project.name }}}
# {{{ project.license }}}

artwork:
	_bin/artwork.sh

depends:
	_bin/depends.sh

new:
	_bin/new.py

minify:
	java -jar ~/Library/Code/compiler.jar --js _site/js/main.js --js_output_file js/main.min.js

publish:
	ssh {{{ project.login }}}@{{{ production.host }}} "{{{ project.login }}}/_bin/publish.sh"

serve:
	bundle exec jekyll serve

incremental:
	bundle exec jekyll clean
	bundle exec jekyll serve --incremental

build:
	JEKYLL_ENV=production bundle exec jekyll build

production:
	JEKYLL_ENV=production bundle exec jekyll serve

.PHONY: artwork depends new minify publish serve incremental build production
