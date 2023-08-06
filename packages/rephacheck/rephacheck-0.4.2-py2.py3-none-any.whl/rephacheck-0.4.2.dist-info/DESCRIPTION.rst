Health check for PostgreSQL + repmgr
====================================

This package is intended to be used as an health check backend for HAProxy. It
provides a small script that will run an HTTP server querying each PostgreSQL
servers of the replication cluster to know the role (primary, standby, witness
or fenced) of the local instance according to the majority of them (kind of a
vote).

Usage and configuration example to come…


