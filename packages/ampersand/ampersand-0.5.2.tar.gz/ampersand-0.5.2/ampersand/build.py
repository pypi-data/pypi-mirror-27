from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import range
from builtins import str
from future import standard_library
standard_library.install_aliases()

import sys, os, json, pystache, shutil, errno
p = os.path # Aliasing os.path to 'p'

def relative(origin):
    def joined (*to):
        path = origin

        for t in to:
            path = os.path.join(path, t)

        return path

    return joined

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def copy_content(src, dest):
    if os.path.exists(src):
        try:
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        except OSError as exc:
            try:
                if exc.errno == errno.ENOTDIR:
                    shutil.copy(src, dest)
                else: raise
            except OSError as e:
                print("Couldn't copy: %s" % str(e))
    else:
        print("Source path doesn't exist: %s" % src)

def path_name(path):
    return os.path.basename(os.path.normpath(path))

def get_json(path):

    # Load a JSON file into a dictionary
    try:
        return json.loads(read_file(path))

    except ValueError as e:
        print("Failed to get JSON from '%s': %s" % (path, str(e)))
        sys.exit()

def get_content(path):

    # Collect front matter and content
    page = read_file(path)
    page = page.split("}}}", 1)

    # Load front matter into a dictionary
    try:
        content = page[1]
        try:
            frontmatter = json.loads("{ %s }" % page[0])
        except ValueError:
            frontmatter = {}
    except IndexError:
        content = page[0]
        frontmatter = {}

    return (frontmatter, content)

def build_file(modal, new_file, content):

    # Render the template HTML file
    new_content = pystache.render(read_file(modal), content)

    # Generate the new file using the template
    try:
        generated = open(new_file, "w")
    except IOError:
        os.makedirs(p.dirname(new_file))
        generated = open(new_file, "w")

    generated.write(new_content)
    generated.close()

def amp_new(args):
    # Builds a new Ampersand project

    if args[2][0] is not "-":
        i = 2
        name = args[i]
    else:
        i = 3
        name = args[i]

    lang = "en"
    if len(args) > i + 1:
        lang = args[i + 1]

    print("Creating new site '%s'" % (name))

    # Build the project tree
    print(" * Building tree")
    tree = [
        "_modals", "_trans", p.join("_trans", lang),
        "_includes", "_site", "_plugins"
    ]
    try:
        os.mkdir(args[2])
    except FileExistsError as e:
        print(str(e))
        sys.exit()

    for folder in tree:
        os.mkdir(os.path.join(name, folder))

    # Create empty files
    abspath = p.dirname(p.abspath(__file__))
    open(p.join(name, "_modals", "index.html"), "a+").close()
    build_file(p.join(abspath, "templates", "page.json"),
                     p.join(args[2], "_trans", lang, "index.json"),
                     {})

    # Build the _ampersand.json file
    print(" * Building _ampersand.json")
    build_file(
        p.join(abspath, "templates", "_ampersand.json"),
        p.join(args[2], "_ampersand.json"), {
            "name": name,
            "lang": lang
        })

    print("Created boilerplate website.")

def collect(site):
    # Create variables pointing to items in the configuration
    root = relative(site.root)
    config = site.config

    content = {}

    # Collect the translation's files into a list
    lang = [name for name in
           os.listdir(root(config["translations"]))
           if p.isdir(root(config["translations"], name))]

    for directory in lang:
        # Looping through the language directories
        lang_dir = root(config["translations"], directory)
        pages = []

        # Iterate through directories and subdirectories
        for path, dirs, files in os.walk(p.join(config["translations"], )):
            # Iterate through each file
            for f in files:
                # Skip '_trans/lang' when taking the path
                f_list = os.path.normpath(p.join(path, f)).split(p.sep)
                pages.append(p.join(*f_list[2:]))

        content[directory] = {}

        for page in pages:
            # Looping through the pages
            if not p.isdir(page):
                # Getting the front matter
                try:
                    trans = json.loads(read_file(p.join(lang_dir, page)))
                    page_content = {}
                    try:
                        frontmatter = trans["_frontmatter"]
                    except KeyError:
                        continue
                except ValueError as e:
                    trans = {}
                    text = get_content(p.join(lang_dir, page))
                    if not text[0]:
                        if site.verbose: print(" ** Skipping '%s': '%s'" % (page, str(e)))
                        continue
                    frontmatter = text[0]
                    page_content = text[1]

                # Getting the global translations
                try:
                    _global = get_json(p.join(lang_dir, "_global.json"))
                except (IOError, OSError):
                    _global = {}

                includes_files = os.listdir(root(config["includes"]))
                includes = {}

                for i in range(len(includes_files)):
                    # Read the layout into "contents"
                    contents = read_file(root(config["includes"],
                                              includes_files[i]))

                    # Render the includes using _ampersand.json and _global.json
                    includes[p.splitext(includes_files[i])[0]] = pystache.render(
                        contents, {
                        "frontmatter": frontmatter, "trans": trans,
                        "content": content, "config": config,
                        "global": _global,

                    })

                content[directory][page] = {
                    "frontmatter": frontmatter, "trans": trans,
                    "content": page_content, "includes": includes,
                    "config": config, "global": _global
                }

    return content

def build_pages(content, site):
    config = site.config
    root = relative(site.root)

    # Iterate through the plugins
    try:
        if config["plugins"] is not False:
            print(" * Passing content to the plugins")
            for key, value in sorted(config["plugins"].items()):
                if site.verbose: print(" ** Running %s" % key)
                site.plugin_run(key, "builder", content)

    except (KeyError, TypeError):
        pass

    try:
        for item in config["manifest"]:
            copy_content(
                root(item)
              , root(config["site"]
                  , path_name(item)))

    except KeyError:
        pass

    for lang in sorted(content.keys()):
        # Loop through each language dictionary

        for page in sorted(content[lang].keys()):
            # Loop through each page
            if content[lang][page]["frontmatter"] == {}:
                print(" ** Skipping '%s': Error in the front matter" % page)
                continue

            # Build the pages
            fm = content[lang][page]["frontmatter"]
            try:
                if site.verbose: print(" ** Generating '%s'" % page)

                if lang != config["primary"]:
                    file_path = root(config["site"], lang, fm["url"])
                else:
                    file_path = root(config["site"], fm["url"])

                build_file(root(config["modals"], fm["modal"]),
                           file_path,
                           content[lang][page])

            except OSError as e:
                print(" ** Skipping '%s': %s" % (page, str(e)))
