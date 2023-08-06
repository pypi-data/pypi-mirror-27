# coding: utf8
import urllib


def _need_loop(v):
    """
    if a variable should loop to concat string
    :param v: any variable
    :return: Boolean
    """
    return isinstance(v, list) or isinstance(v, dict) or isinstance(v, tuple)


def recursive_urlencode(d):
    """
    Use me only!

    convert a nested dict or list or tuple or nested of that
    to string.

    PHP $_POST will accept these parameters as nested array:
    http://php.net/manual/en/faq.html.php#faq.html.arrays

    modified from: https://stackoverflow.com/a/4014164/2752670

    :param d: nested dict or list or tuple
    :return: String
    """

    def add_item_str(key, value, base):
        pairs = []
        new_base = base + [key]
        if _need_loop(value):
            pairs += recursion(value, new_base)
        else:
            if len(new_base) > 1:
                first = urllib.quote(str(new_base.pop(0)))
                rest = map(lambda x: urllib.quote(x), (str(x) for x in new_base))
                new_pair = "%s[%s]=%s" % (
                    first,
                    ']['.join((str(x) for x in rest)),
                    urllib.quote(unicode(value))
                )
            else:
                new_pair = "%s=%s" % (urllib.quote(unicode(key)), urllib.quote(unicode(value)))
            pairs.append(new_pair)
        return pairs

    def recursion(d, base=[]):
        pairs = []

        if isinstance(d, dict):
            for key, value in d.items():
                pairs += add_item_str(key, value, base)
        elif isinstance(d, list) or isinstance(d, tuple):
            for key, value in enumerate(d):
                pairs += add_item_str(key, value, base)
        return pairs

    return '&'.join(recursion(d))
