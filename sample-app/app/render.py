"""Render invoice summaries with plain string templates (Jinja2 is no longer used)."""
from string import Template

SUMMARY = Template("Invoice $number for $customer: EUR $total")


def summary(invoice):
    return SUMMARY.substitute(invoice)
