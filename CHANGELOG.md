# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [Unreleased]

## [1.2.0] - 2021-02-21

### Changed

-   Made zstd support optional. zstd support can be installed with `pip install pytiled-parser[zstd]`. PyTiled will raise a ValueError explaining to do this if you attempt to use zstd compression without support for it installed. This change is due to the zstd library being a heavy install and a big dependency to make mandatory when most people probably won't ever use it, or can very easily convert to using gzip or zlib for compression.

## [1.1.0] - 2021-02-21

### Added

-   Added support for zstd compression with base64 encoded maps
-   Better project metadata for display on PyPi

## [1.0.0] - 2021-02-21

Initial Project Release
