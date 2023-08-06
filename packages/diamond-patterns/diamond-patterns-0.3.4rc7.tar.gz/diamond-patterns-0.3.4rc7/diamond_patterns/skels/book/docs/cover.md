# Cover

Ian Dennis Miller
2017

## source files in `artwork/cover`

Various covers may be specified depending on the width of the spine, which is determined by the total page count.  For 161-170 pages, use the `170p` spine.

- `170p/blah.svg`

## calculations for cover

The cover is a single sheet that wraps the front, back, and spine of a book.  Since the spine width is determined by how thick the spine is, and the number of pages in the book determines thickness, you cannot know how wide the cover is until you know how many pages you have.

**spine width calculation: multiply page count by 0.002252**

CreateSpace has a cover template builder here:

https://www.createspace.com/Help/Book/Artwork.do

### 130 pages

126 pages, rounded up to 130.

- 130 pages at 0.002252 per page = .29276
- width: .125 + 5.5 + .29276 + 5.5 + .125 = 11.54276
- height: .125 + 8.5 + .125 = 8.75

### 160 pages

157 pages, rounded up to 160.

- 160 pages at .002252 per page = .36032
- width: .125 + 5.5 + .36032 + 5.5 + .125 = 11.61032
- height: .125 + 8.5 + .125 = 8.75

### 170 pages

163 pages, rounded up to 170.

- 170 pages at .002252 per page = .38284
- width: .125 + 5.5 + .38284 + 5.5 + .125 = 11.63284
- height: .125 + 8.5 + .125 = 8.75

## print cover as letter-sized nobleed

For home printing, the cover needs to fit on a letter sheet of paper.  This basically works as long as the book is milled to 5.25 x 8.5, because the 0.5 inches you cut off is about equivalent to the spine.

To center the cover on a letter sheet:

- 11.53375 - 11 = 0.53375
- 0.53375 / 2 = 0.266875
- thus, the x position for an 8.5x11 export region in the source SVG is 0.266875
