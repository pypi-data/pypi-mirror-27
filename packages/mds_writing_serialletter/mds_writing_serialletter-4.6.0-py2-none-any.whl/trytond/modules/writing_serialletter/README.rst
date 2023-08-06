serial letters
==============
- a Tryton module to write serial letters for paper-based newsletters
- create a letter-template with placeholders
- export a Libreoffice-Writer-file or PDF-file from the letter-template, individually for each recipient

Install
=======
  pip install mds-writing-serialletter

Requires
========
- Tryton 4.6
- mds-party-fieldaddon

How to use
==========
Grant access to serial-letter
#############################
- The group *Serial letter - view* grants read access to the serial letter.
- The group *Serial letter - edit* grants read/write access to the serial letter.
- The group *Party Administration* allows the user to create *salutations* and *greetings*.

Create some salutations and greetings
#####################################
In *Party/Configuration*, open *Salutation* and create a few salutation, something like 'Mr.', 'Mrs.', etc.
Then open *Greetings* and create something like 'Dear', 'Hello', etc.

Create serial letter template
#############################
In *Writing*, open *Serial Letter* and create a new entry. Enter *name* and *subject*. Enter a *contact* to your serial letter. 
Insert text and use placeholders to place recipient-specific texts.

The result could look like this::

  [party:correspondence]
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam 
  nonumyeirmod tempor invidunt...

  sincerely
  [contact:name]

Add recipients
##############
Click *Recipient* and add some recipients. A party can have several addresses, one of these addresses must be marked as a mailing address. Click the button *Activate mailing address* to mark the first address as the mailing address.
For the individual recipients, select the salutations and greetings (double-click the receiver, select und save).

Export
######
Click the report button to get a LibreOffice-Writer-file from your mailing.

Changes
=======

*4.6.0 - 12/15/2017*

- compatibility to Tryton 4.6 + Python3

*0.1.3 - 06/14/2017*

- updated depency

*0.1.2 - 06/07/2017*

- module name changed

*0.1.1 - 05/26/2017*

- first public version
