# cdm-gc-plugin
The project is a [Codimension Python IDE](http://codimension.org) garbage collector plugin.

The idea of the plugin is simple. The embedded Python garbage collector triggers objects collection at pretty
much unknown moments and the plugin will make it more predictable. The plugin will call the
**`collect()`** method of the Python gc module when:

- a tab is closed
- a project is changed
- new files appeared in a project
- some files are deleted from a project

There is pretty much no user interface for the plugin. It does its work in the background.


# Installation
The plugin is pip installable:

```bash
pip install cdmgcplugin
```

There is a little value (if any) to install it without the [Codimension IDE](http://codimension.org).
It however can be a good start point in developing a new plugin for Codimension. The overall structure
could be copied as well as the way the plugin is installed.
