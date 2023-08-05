from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import input
from builtins import str
from future import standard_library
standard_library.install_aliases()

from ampersand import build
from shutil import rmtree
import sys, os, json, subprocess, importlib, inspect
p = os.path

class Ampersand(object):

    """docstring for Ampersand."""

    def __init__(self, verbose):

        # Attempt to find the _ampersand.json configuration file
        try:
            config = build.get_json("_ampersand.json")
            root = p.dirname(p.abspath("./_ampersand.json"))

        except OSError:
            # Ask the user where to find the _ampersand.json file

            try:
                location = input("Enter the path (from here) to the root of "
                                + "your project: ")
                config = build.get_json(p.join(location, "_ampersand.json"))
                root = p.abspath(location)

            except (KeyboardInterrupt, OSError) as e:

                print(str(e))
                sys.exit()

        self.root = root
        self.config = config
        self.verbose = verbose

    def serve(self):

        print(" * Collecting all pages")

        pages = build.collect(self)

        # Build the pages
        print(" * Building pages")
        build.build_pages(pages, self)

        print("Done.")

    def plugin_add(self, url):
        root = relative(self.root)

        try:
            # Decide on what to call the plugin and its path
            plugin = p.split(url)[1]
            plugin_path = root(self.config["modules"], plugin)

            # Download the plugin via git
            print("Installing Ampersand plugin '%s'" % plugin)
            try:
                clone = subprocess.check_call(["git", "clone", url, plugin_path])

                try:
                    plugins_dict = self.config["plugins"]
                except KeyError:
                    self.config["plugins"] = {}
                    plugins_dict = self.config["plugins"]

                # Update the _ampersand.json file by adding the plugin
                plugins_dict[p.basename(plugin)] = p.join(
                    self.config["modules"], plugin )
                with open(p.join(self.root, "_ampersand.json"), "w", encoding="utf-8") as updated:
                    updated.write(json.dumps(self.config, indent=4, ensure_ascii=False))
            except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
                print(str(e))
                sys.exit()

        except KeyError as e:
            print("Missing entry in your configuration file: %s" % str(e))

    def plugin_remove(self, name):
        root = relative(self.root)

        try:
            # Delete the directory containing the plugin
            print("Removing plugin '%s'" % name)
            rmtree(root(self.config["modules"], name ))
        except FileNotFoundError:
            pass
        except (IOError, OSError) as e:
            print(str(e))
            print("Couldn't remove plugin. You may need to delete it manually.")

        try:
            # Update _ampersand.json by adding the plugin
            self.config["plugins"].pop(name)
            with open(root("_ampersand.json"), "w", encoding="utf-8") as updated:
                    updated.write(json.dumps(self.config, indent=4, ensure_ascii=False))
        except KeyError:
            print("Failed to remove plugin '%s' as it is not installed." % name)
            sys.exit()

    def plugin_run(self, name, method, content):
        root = relative(self.root)

        try:
            # Retrieve the _plugin.json file
            plugin = build.get_json(
                root(self.config["plugins"][name], "_plugin.json"))

            # Load and run the module
            if plugin["method"] == method:
                sys.path.append(root(self.config["plugins"][name]))
                module = importlib.import_module(plugin["init"], name)
                content = module.main(content, self)

            return content

        except (KeyError, OSError, TypeError,
                ImportError, AttributeError) as e:
            return content
