# RSS Groups

RSS Groups are a way to mix multiple RSS feeds together, creating a
single feed that can be subscribed to.

This is a simple idea, but it allows new RSS feeds to be added to a
group and automatically be included in the group feed, instead of
having to be followed individually. This means that everyone
subscribed to the group's feed can know they are seeing the same
posts.

This code implements a website that creates a group and its feed and
allows new feeds to be added. It also supports customized, private
feeds, so that only users who have been approved can see the feed.

## User Experience

An RSS Group fulfills a similar function to a Facebook group. Members
can read the group's feed to see everybody's posts. When they want to
add their own, they post to their own blog with its feed attached to
the group.

If the group is configured to only proivide private RSS feeds, then
only members who have been given one of these private feeds will be
able to read it. Combined with private blogs, this creates the effect
of a private group. RSS Groups can also create a public RSS feed,
which would allow anyone to read, though not post.

## Platform Choice

Any RSS feed is supported. However, these are normally public. For
private groups, authentication is required.

Some blogging software is compatible with RSS, using methods like
Basic Authentication. RSS Groups support this. For other blogging
software, there is no simple RSS interface to private feeds, so
special plugins must be written.

Of blogging platforms that do not provide private RSS feeds, RSS
Groups support:
-  Wordpress
-  Google Blogger

## Future Work

Future work will depend on how RSS Groups are used and what is
needed. It is likely that some sort of cross-platform reactions
("Like" buttons and similar features) would be valuable.
