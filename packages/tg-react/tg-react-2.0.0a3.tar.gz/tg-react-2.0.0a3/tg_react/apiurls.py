from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
import re

try:
    from django.utils.module_loading import import_string

except ImportError:
    from django.utils.module_loading import import_by_path as import_string


def ucfirst(word):
    return word[0].upper() + word[1:].lower()


def to_camelcase(value):
    value = value.replace(' ', '_').replace('-', '_').lower()

    return "".join([ucfirst(x) if i > 0 else x for i, x in enumerate(value.split('_'))])


def tokenize_pattern(regex):
    if not regex:
        return regex

    pattern_str = regex.pattern

    # Just a matching group, replace with ${argID}
    if not len(list(regex.groupindex.keys())):
        for idx in range(1, regex.groups + 1):
            pattern_str = re.sub(r"\([^\)]+\)", "${arg%s}" % (idx - 1), pattern_str)

    # Replace group match with ${groupName}
    for key, idx in regex.groupindex.items():
        pattern_str = re.sub(r"(\(\?P<%s>)[^\)]+\)" % key, "${%s}" % key, pattern_str)

    return pattern_str.lstrip('^').rstrip('$')


def flatten_patterns(urlconf, base_path=None, namespace=None):
    result = {}

    base_path = base_path or ''
    namespace = namespace or ''
    namespace = '%s:' % namespace if namespace else ''

    if not isinstance(urlconf, (RegexURLResolver, list)):
        raise ImproperlyConfigured('The urlconf provided cannot be flattened.')

    if isinstance(urlconf, RegexURLResolver):
        urlconf = urlconf.url_patterns

    for url in urlconf:
        if isinstance(url, RegexURLPattern):
            if url.name == 'api-noop' or not url.name:
                continue

            url_result = '%s%s' % (base_path, tokenize_pattern(url.regex))

            result['%s%s' % (namespace, to_camelcase(url.name))] = url_result

        elif isinstance(url, RegexURLResolver):
            flattened = flatten_patterns(
                url,
                base_path=base_path + (tokenize_pattern(url.regex) or ''),
                namespace=namespace + (url.namespace or '')
            )

            for key, value in flattened.items():
                result[key] = value

    return result


def flatten_urls(module_path, base_path):
    if not module_path.endswith('urlpatterns'):
        module_path += '.urlpatterns'

    return flatten_patterns(import_string(module_path), base_path=base_path)
