# -*- encoding: utf8 -*-
# © Toons

"""
Usage: 
    delegate link <secret> [<2ndSecret>]
    delegate unlink
    delegate status
    delegate voters
    delegate forged

Subcommands:
    link   : link to delegate using secret passphrases. If secret passphrases
             contains spaces, it must be enclosed within double quotes
             (ie "secret with spaces").
    unlink : unlink delegate.
    status : show information about linked delegate.
    voters : show voters contributions ([address - vote] pairs).
    forged : show forge report.
"""

import arky

from .. import cfg
from .. import rest
from .. import util

from . import DATA
from . import input
from . import checkSecondKeys
from . import checkRegisteredTx

from .account import link as _link
from .account import unlink # as _unlink

import io
import os
import sys
import collections


def _whereami():
	if DATA.account and not DATA.delegate:
		_loadDelegate()
	if DATA.delegate:
		return "delegate[%s]" % DATA.delegate["username"]
	else:
		return "delegate"


def _loadDelegate():
	if DATA.account:
		resp = rest.GET.api.delegates.get(publicKey=DATA.account["publicKey"])
		if resp["success"]:
			DATA.delegate = resp["delegate"]
			return True
		else:
			return False


def link(param):
	_link(dict(param, **{"--escrow":False}))
	if not _loadDelegate():
		sys.stdout.write("Not a delegate\n")
		unlink(param)


# def unlink(param):
# 	_unlink(param)


def status(param):
	if DATA.delegate:
		util.prettyPrint(dict(DATA.account, **DATA.delegate))


def forged(param):
	if DATA.delegate:
		resp = rest.GET.api.delegates.forging.getForgedByAccount(generatorPublicKey=DATA.account["publicKey"])
		resp.pop("success")
		util.prettyPrint(resp)


def voters(param):
	if DATA.delegate:
		accounts = rest.GET.api.delegates.voters(publicKey=DATA.delegate["publicKey"]).get("accounts", [])
		sum_ = 0.
		log = collections.OrderedDict()
		for addr, vote in sorted([[c["address"], float(c["balance"]) / 100000000] for c in accounts], key=lambda e:e[-1]):
			log[addr] = "%.3f" % vote
			sum_ += vote
		log["%d voters"%len(accounts)] = "%.3f" % sum_
		util.prettyPrint(log)
