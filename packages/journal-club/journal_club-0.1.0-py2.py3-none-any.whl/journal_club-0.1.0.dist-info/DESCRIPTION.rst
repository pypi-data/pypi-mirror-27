
A command line interface to a  weighted scheme to select a person to present at a journal club

Install with ``pip install journal_club``
Use with:
.. code-block:: bash
    $ jc create person1 person2 person3 ...

    $ jc choose person1 person2

This creates a csv with 3 people and then chooses between them. 
The act of choosing updates the record of who was there.

