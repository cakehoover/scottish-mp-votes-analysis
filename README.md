A set of scripts to find the votes in the House of Commons since 1997 where

Best run in the following order:

* `get_constituencies_pre_2005.py` - Scrapes pre-2005 constituencies from Wikipedia.
* `get_constituencies_post_2005.py` - Gets post-2005 constituencies from Wikipedia.
* `get_divisions.py` - Gets all Commons divisions since 1997 from PublicWhip.
* `get_votes.py` - For each division, checks whether the vote result would have been
  different if votes from Scottish constituencies had not been counted.