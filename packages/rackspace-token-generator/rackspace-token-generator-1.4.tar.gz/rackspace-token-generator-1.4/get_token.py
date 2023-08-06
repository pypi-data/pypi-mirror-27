#! /usr/bin/env python

import argparse
from getpass import getpass
import sys

from keystoneauth1 import exceptions
from keystoneauth1 import session
from rackspaceauth import v2 as auth


def _main():
    parser = argparse.ArgumentParser(
        description="Generate a Rackspace Cloud Identity "
                    "authentication token",
        epilog="When providing a password or an API key, you must "
               "provide a username. When providing an existing "
               "token, you must provide a tenant id. "
               "You will be prompted to enter the "
               "password, API key, or token you are "
               "authorizing yourself with after providing the "
               "username or tenant id.")

    types = parser.add_mutually_exclusive_group(required=True)
    types.add_argument("--password", dest="use_password",
                       action="store_true",
                       help="Rackspace Cloud Identity Password")
    types.add_argument("--api-key", dest="use_api_key",
                       action="store_true",
                       help="Rackspace Cloud Identity API Key")
    types.add_argument("--token", dest="use_token",
                       action="store_true",
                       help="Rackspace Cloud Identity API Key")

    ids = parser.add_mutually_exclusive_group(required=True)
    ids.add_argument("--username", dest="username",
                     help="Rackspace Cloud Identity Username")
    ids.add_argument("--tenant-id", dest="tenant_id",
                     help="Rackspace Cloud Tenant ID")

    parser.add_argument("--reauthenticate", dest="reauthenticate",
                        action="store_true", default=True,
                        help="Rackspace Cloud Identity API Key")

    args = parser.parse_args()

    if args.use_password and args.username is not None:
        password = getpass("Enter password: ")
        authenticator = auth.Password(username=args.username,
                                      password=password,
                                      reauthenticate=args.reauthenticate)
    elif args.use_api_key and args.username is not None:
        api_key = getpass("Enter API key: ")
        authenticator = auth.APIKey(username=args.username,
                                    api_key=api_key,
                                    reauthenticate=args.reauthenticate)
    elif args.use_token and args.tenant_id is not None:
        token = getpass("Enter token: ")
        authenticator = auth.Token(tenant_id=args.tenant_id,
                                   token=token)
    else:
        print("*** Error: "
              "No authentication method could be created from "
              "the given arguments")
        parser.print_help()
        return 1

    s = session.Session(auth=authenticator)
    try:
        token = s.get_token()
    except exceptions.http.Unauthorized:
        print("Authentication failed")
        return 2
    else:
        print("Token:\n  %s" % token)

    return 0


if __name__ == "__main__":
    sys.exit(_main())
