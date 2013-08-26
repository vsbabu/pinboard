## Simple HTML Viewer for lists

When you've multiple lists to manage and you don't want a cross platform, web syncing stuff like google keep!

I maintain my lists using [VIM](http://www.vim.org/), much easier than all list-managers out there. This html+js combo just takes that
list and displays in a nice (IMHO) view. 

![Obligatory screenshot](ss2013-06-08.png)

## Installation
Just unzip all files to a folder. Open `index.html` in a browser. Tested in Chrome and Firefox.

## Usage

Edit `board.js.yml`. Any good text editor will do. Syntax is YAML.

Each box has a title, color and items. Each item is indented and with a hyphen followed by a space.

An item can have the following markers after the hyphen and space.

  1. hyphen (-) will put a strikethrough the text. Good for showing done items.
  2. carat (^) will put a flag. Put more ^ for showing more flags.
  3. tilde (~) will put a mail icon. Put more ~ if needed. This can indicate wip items.

## Dependencies & Credits

  * [JQuery](http://jquery.com/) - linked from `index.html`.
  * [JQuery Masonry](http://masonry.desandro.com/) - linked from `index.html`.
  * [yaml.js](https://bitbucket.org/jeremyfa/yaml.js/overview) - included because I thought direct linking to a repository is not nice.
  * [Fam Fam icons](http://www.famfamfam.com/lab/icons/mini/) - 2 icons linked from `board.css`.

If you want to run all of these locally so that you want to view it without net connection, get local copies of these files.


