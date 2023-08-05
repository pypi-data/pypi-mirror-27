# (cc) 2017 diamond-patterns

new:
	_bin/template.py

artwork:
	_bin/artwork.sh

depends:
	_bin/depends.sh

githooks:
	_bin/git/githooks.sh

init:
	_bin/git/init.sh

clean:
	bundle exec jekyll clean

js:
	java -jar ~/Library/Code/compiler.jar --js _site/js/main.js --js_output_file js/main.min.js

serve:
	bundle exec jekyll serve

incremental: clean
	bundle exec jekyll serve --incremental

build:
	JEKYLL_ENV=production bundle exec jekyll build

production:
	JEKYLL_ENV=production bundle exec jekyll serve

.PHONY: artwork depends new js serve incremental build production githooks clean init
