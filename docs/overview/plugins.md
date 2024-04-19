# Plugins

## About plugins

Plugins are how Lungo extends its functionality. They are applications that run within containers alongside Lungo,
offering additional services to users. Each plugin can be independently enabled or disabled, with its own configuration.

Lungo has built-in plugins for several popular applications. You can also install custom plugins or even develop your
own.

Please be aware that insecure or malicious plugins may compromise the security of not only your Lungo instance but also
your entire system. Therefore, it is strongly advised to install plugins exclusively from trusted sources.

## Built-in plugins

| Application                                                      | Value         | Status                                          |
|:-----------------------------------------------------------------|---------------|:------------------------------------------------|
| [File Browser](https://filebrowser.org/)                         | `filebrowser` | :material-check-circle-outline:{ .icon .green } |
| [JupyterHub](https://jupyter.org/hub)                            | `jupyterhub`  | :material-check-circle-outline:{ .icon .green } |
| [PrivateBin](https://privatebin.info/)                           | `privatebin`  | :material-check-circle-outline:{ .icon .green } |
| [RStudio](https://posit.co/products/open-source/rstudio-server/) | `rstudio`     | :material-check-circle-outline:{ .icon .green } |
| [Stirling PDF](https://stirlingtools.com/)                       | `stirlingpdf` | :material-check-circle-outline:{ .icon .green } |
| [Xray](https://xtls.github.io/)                                  | `xray`        | :material-check-circle-outline:{ .icon .green } |

Legend:

| Icon                                              | Meaning             |
|:--------------------------------------------------|:--------------------|
| :material-check-circle-outline:{ .icon .green }   | Fully supported     |
| :material-alert-circle-outline:{ .icon .yellow }  | Partially supported |
| :material-clock-time-four-outline:{ .icon .blue } | Planned             |
