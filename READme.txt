ThresHold can then be run with the click of the button via the threshold_gui.py file
simply press run under threshold_gui and follow the fields accordingly

The input txt file must be present in the following format:

    Hugo_Symbol     Entrez_Gene_Id      {Patient1ID}    {Patient2ID}...
    ...             ...                 zscores...      zscores...
    ...             ...                 ...             ...

    The Entrez_Gene_Id column is never actually used so as long as there is a space between the Hugo_Symbol and Patient1 column it will run.
    Note the first heading MUST be called Hugo_Symbol

See additional documentation for info regarding how values are calculated