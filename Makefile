# Makefile for source rpm: irqbalance
# $Id$
NAME := irqbalance
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
