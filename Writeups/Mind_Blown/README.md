# Mind Blown
Forensics

## Challenge 

One of my friends keeps sending me weird memes from his favorite subreddit but I don't quite understand this one...

[meme](694003b3deecf2382b3aa510e5f3e5f5153bb9c062e4f20878c0d343bc297767_meme.jpg)

## Solution

If you observe the thumbnail of the file and the original image, they are different.

We can extract the thumbnail using ExifTool

https://stackoverflow.com/a/39125561

In this case, the thumbnail also contains another thumnbnail which is the flag
	
	$ exiftool -a -b -W %d%f_%t%-c.%s -preview:all meme.jpg
	    1 output files created
	$ exiftool -a -b -W %d%f_%t%-c.%s -preview:all meme_ThumbnailImage.jpg
	    1 output files created

## Flag

	tjctf{kn0w_y0ur_m3tad4ta}
