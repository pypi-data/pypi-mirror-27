#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from uuid import uuid4
from cdumay_rest_client.exceptions import HTTPException


class Result(object):
    def __init__(self, retcode=0, stdout="", stderr="", retval=None, uuid=None):
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr
        self.retval = retval or dict()
        self.uuid = uuid if uuid else uuid4()

    def print(self, data):
        """Store text in result's stdout

        :param Any data: Any printable data
        """
        self.stdout += "{}\n".format(data)

    def print_err(self, data):
        """Store text in result's stderr

        :param Any data: Any printable data
        """
        self.stderr += "{}\n".format(data)

    @staticmethod
    def fromException(exc, uuid=None):
        """ Serialize an exception into a result

        :param Exception exc: Exception raised
        :param str uuid: Current Kafka :class:`kser.transport.Message` uuid
        :rtype: :class:`kser.result.Result`
        """
        if not isinstance(exc, HTTPException):
            exc = HTTPException(code=500, message=str(exc))

        return Result(
            uuid=exc.extra.get("uuid", uuid or uuid4()),
            retcode=exc.code, stderr=exc.message,
            retval=dict(error=exc)
        )

    def __add__(self, o):
        """description of __add__"""
        self.retcode = self.retcode if self.retcode > o.retcode else o.retcode
        self.retval.update(o.retval)
        if len(o.stdout) > 0:
            self.stdout += "\n{}".format(o.stdout)
        if len(o.stderr) > 0:
            self.stderr += "\n{}".format(o.stderr)
        return self

    def __str__(self):
        return self.stdout if self.retcode == 0 else self.stderr

    def __repr__(self):
        return "Result<retcode='{}'>".format(self.retcode)
