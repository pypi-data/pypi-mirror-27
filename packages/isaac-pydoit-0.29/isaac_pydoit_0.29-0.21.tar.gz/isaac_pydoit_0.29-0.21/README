A super-simple modification to pydoit to make its uptodate check behave more like Make.

Instead of considering a file changed if the timestamp of a dependency differs at all, pydoit can now consider a file changed only if the timestamp of the dependency is newer than the one in its database.

I wanted this because I have processing code that takes a long time. And I want to be able to re-write code upstream of that processing stuff without being forced to reprocess everything. Instead, I can simply ">> touch -d '2 days ago' myfile.py" and be the dependency will still be seen as unmodified.

A tradeoff between the most strict (any timestamp modification is seen as a change) and most flexible (I still have to make a conscious effort and touch the file if I don't want the code to be seen as modified)
