# About

Package to use BioMAJ providing biomaj-cli

# Example

    biomaj-cli.py --proxy http://biomaj-public-proxy --api-key XYZ_MYAPIKEY --update --bank Anopheles_gambiae

To get help usage:

    biomaj-cli -h

 If proxy is not specifed, a monolitic and local BioMAJ installation is expected

 To create users, see biomaj-user repo or BioMAJ wiki


3.1.9:
  Add option --stats, needs biomaj-daemon >= 3.0.13
  Add option --json, needs biomaj-daemon >= 3.0.13
3.1.8:
  Add option --schedule
3.1.7:
  If no arg given, display help
3.1.6:
  Add options --last-log and --tail to get last log of a bank, needs biomaj-daemon >= 3.0.8
3.1.5:
  Add missing biomaj-core req
3.1.4:
  Add whatsup option
  Fix default value for --config
3.1.2:
  Add missing README
  Fix for monolithic usage
3.1.1:
  Use biomaj daemon utils for options management
  Fix config setup when using local install
  Rename biomaj-daemon-cli to biomaj-cli
3.1.0:
  Create client for biomaj with micro services


