#!/bin/bash

ldapsearch -x -H ldap://localhost \
  -b ou=users,dc=example,dc=org \
  -D "cn=admin,dc=example,dc=org" \
  -w password \
  "uid=jane.doe"
