# Silbacre

Silbacre (SILence BACkup REader) is an API for reading backup files from [Silence](https://silence.im) (previously known as SMSSecure).

Silbacre is most easily used casually as a script.

    silbacre /path/to/backup.xml

That will provide what looks like a normal Python console (`code.interact()`), but some variables are pre-defined. The most commonly used variable will of course be the messages themselves. They are, as can be expected `messages`. This is a list of dictionaries. (Described below under the heading *Message keys*.)

## Searching

A class is also defined called `SearchTerm`. This can be used with the convenience function `search`. The `SearchTerm` supports the `&` and `|` binary operators with tuples or other SearchTerms. An example to check for messages containing `'morning'` that were sent in the afternoon is below:

    >>> def is_afternoon(date):
    ...     return date.hour >= 12
    ...
    >>> has_morning = SearchTerm(('body', 'morning', None))
    >>> search(has_morning & ('date', is_afternoon, Search.function))

The first argument is which key of the message is being checked. The second is the value it should match, and the third is how to define a match. The options are `Search.lowercase`, `Search.regex`, and `Search.function`.

The default (`None`) is `Search.lowercase`, which just sees if `'hello'` (in any capitalization) is found in the body.

If instead of checking containment, you have a more complicated check, you could use `Search.regex`, in which case `re.match()` is used.

The last gives more customization. Instead of providing a string as what should be matched, a function is given (or any callable) and the type is set as `Search.function`. The function will be given `message[key]`, where `key` is of course the first argument, in our case `'date'` (which is a `datetime.datetime` object as described below in *Message keys*). The function should then return True for a successful match or False for a no-match.
    

## Message keys

The keys in each message dictionary are the same as in the original XML file except for these changes:

* `name` is the name of the contact if a contacts .vcf file is provided and the contact is found. Otherwise, same as `address`. Note that contacts with pictures are not recognized by `strudel`, the VCard parsing library used. (I am happy to hear recommendations for a better library.)
* `address` is the phone number of the contact. Silence does not standardize the format, so Silbacre does (with `phonenumbers`, a port of Google's excellent library). An example number in the standardized format would be `(121) 222-3333`
* `date` in the original backup is a number. For example, 1478026211916 is the date of one of my messages. All but the last three digits are what form the seconds since the Epoch. Beyond that is what's after the decimal: 1478026211.916. To make it easier, Silbacre just converts that to a `datetime.datetime` object.

The following table describes all keys. (Italicized are the keys that are in the original backup, but I have found no explanation for.)


key | definition
------ | ------
*protocol* | *Always `'0'`*
address | Phone number of contact
date | `datetime.datetime` object
type | `'1'` for a message sent from the backup owner; `'2'` for a message received
*subject* | *Always `'null'`. Presumably would be used for e-mail MMS messages, but the backup includes only SMS, so I'm in the dark.*
body | Text of the message
*toa* | *Always `'null'`*
*sc_toa* | *Also always `'null'`*
*service_center* | *You guessed it: `'null'`*
read | Whether the message has been marked read. Almost always `'1'` unless you like to ignore your notifications.
*status* | *Always `'-1'`*
locked | Whether the message was encrypted. (`'1'` for yes, `'0'` for no.)
