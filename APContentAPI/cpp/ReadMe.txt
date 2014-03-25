Usage is very straightforward:

  --help                           produce help message
  -m [ --media_type ] arg (=photo) set media type
  -q [ --query ] arg               set search query

The program will output the number of found items along with the title of all entries in the result set.

Note that the project requires these Nuget packages be installed:

Boost
Boost Program Options for Visual Studio 2013
C++ Rest SDK (Casablanca)

Here's the packages.config file:

<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="boost" version="1.55.0.16" targetFramework="Native" />
  <package id="boost_program_options-vc120" version="1.55.0.16" targetFramework="Native" />
  <package id="cpprestsdk" version="2.0.0" targetFramework="Native" />
</packages>

