# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [Unreleased]

## [1.4.0] - 2021-04-25

-   Fixes issues with image loading for external tilesets. Previously, if an external tileset was in a different directory than the map file, image paths for the tileset would be incorrect. This was due to all images being given relative paths to the map file, regardless of if they were for an external tileset. This has been solved by giving absolute paths for images from external tilesets. Relative paths for embedded tilesets is still fine as the tileset is part of the map file.

## [1.3.0] - 2021-03-31

-   Added support for Parallax Scroll Factor on Layers. See https://doc.mapeditor.org/en/stable/manual/layers/#parallax-scrolling-factor

-   Added support for Tint Colors on Layers. See https://doc.mapeditor.org/en/stable/manual/layers/#tinting-layers

## [1.2.0] - 2021-02-21

### Changed

-   Made zstd support optional. zstd support can be installed with `pip install pytiled-parser[zstd]`. PyTiled will raise a ValueError explaining to do this if you attempt to use zstd compression without support for it installed. This change is due to the zstd library being a heavy install and a big dependency to make mandatory when most people probably won't ever use it, or can very easily convert to using gzip or zlib for compression.

## [1.1.0] - 2021-02-21

### Added

-   Added support for zstd compression with base64 encoded maps
-   Better project metadata for display on PyPi

## [1.0.0] - 2021-02-21

Initial Project Release
